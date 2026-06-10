import json
import logging
import requests

from odoo import api, models

_logger = logging.getLogger(__name__)


class CrmMentionJob(models.Model):
    _name = 'crm.mention.job'
    _description = 'Mention Lead Scanner'

    # ------------------------------------------------------------------
    # ENTRY POINT — called by cron
    # ------------------------------------------------------------------

    @api.model
    def run_mention_scan(self):
        params = self.env['ir.config_parameter'].sudo()
        breakpoint()
        if not params.get_param('crm_mention_leads.enabled'):
            _logger.info("Mentions to Leads: disabled, skipping scan.")
            return

        # Load config
        product_desc = params.get_param('crm_mention_leads.product_desc', '')
        target_customer = params.get_param(
            'crm_mention_leads.target_customer', '')
        subreddits = params.get_param(
            'crm_mention_leads.subreddits', 'entrepreneur,smallbusiness')
        threshold = int(params.get_param(
            'crm_mention_leads.score_threshold', 60))

        if not product_desc:
            _logger.warning(
                "Mentions to Leads: no product description configured. Run setup wizard.")
            return

        # Step 1 — Generate intent queries via AI
        queries = self._generate_intent_queries(product_desc, target_customer)
        _logger.info("Mentions to Leads: generated %d queries", len(queries))

        # Step 2 — Fetch Reddit posts via ScrapeCreators
        posts = self._fetch_reddit_posts(subreddits.split(','), queries)
        _logger.info("Mentions to Leads: fetched %d posts", len(posts))

        # Step 3 — Score and create leads
        leads_created = 0
        for post in posts:
            # Skip already-processed posts
            if self.env['crm.mention.log'].post_already_processed(post['id']):
                continue

            score, reason = self._score_post(
                post, product_desc, target_customer)

            lead = None
            if score >= threshold:
                lead = self._create_lead(post, score)
                leads_created += 1

            # Always log the post
            self._log_mention(post, score, reason, lead)

        _logger.info(
            "Mentions to Leads: scan complete. %d leads created.", leads_created)

    # ------------------------------------------------------------------
    # STEP 1 — Generate intent queries using Gemini
    # ------------------------------------------------------------------

    def _gemini_generate(self, prompt, temperature=0.3):
        params = self.env['ir.config_parameter'].sudo()
        api_key = params.get_param('crm_mention_leads.gemini_api_key')

        if not api_key:
            raise ValueError("Gemini API key not configured")

        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
            params={"key": api_key},
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": temperature,
                    "responseMimeType": "application/json"
                }
            },
            timeout=30,
        )

        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    def _generate_intent_queries(self, product_desc, target_customer):
        params = self.env['ir.config_parameter'].sudo()
        api_key = params.get_param('crm_mention_leads.gemini_api_key')

        if not api_key:
            return [product_desc[:50]]

        prompt = f"""
You are a B2B sales expert.

Generate 2 short Reddit search queries to find posts where people are
looking for or complaining about problems that this product solves.

Product:
{product_desc}

Target Customer:
{target_customer}

Return ONLY a JSON array.

Example:
[
  "looking for HR software",
  "payroll tool recommendation",
  "replacing BambooHR"
]
"""

        try:
            content = self._gemini_generate(prompt, temperature=0.7)
            return json.loads(content)
        except Exception as e:
            _logger.error(
                "Mentions to Leads: query generation failed: %s", e)
            return [product_desc[:50]]

    # ------------------------------------------------------------------
    # STEP 2 — Fetch Reddit posts via ScrapeCreators API
    # Docs: https://docs.scrapecreators.com/v1/reddit/subreddit/search
    #       https://docs.scrapecreators.com/v1/reddit/search
    # ------------------------------------------------------------------

    def _get_scrapecreators_headers(self):
        """Return auth headers for ScrapeCreators API."""
        params = self.env['ir.config_parameter'].sudo()
        api_key = params.get_param('crm_mention_leads.scrapecreators_api_key')
        if not api_key:
            raise ValueError("ScrapeCreators API key not configured")
        return {"x-api-key": api_key}

    def _parse_scrapecreators_posts(self, data, subreddit_name):
        posts = []

        for item in data.get('posts', []):

            subreddit = item.get('subreddit')

            if isinstance(subreddit, dict):
                subreddit = subreddit.get('name')

            posts.append({
                'id': str(item.get('id', '')),
                'title': item.get('title', ''),
                'body': item.get('selftext') or item.get('body') or '',
                'url': item.get('url', ''),
                'subreddit': subreddit or subreddit_name,
                'author': item.get('author') or item.get('author_name') or '',
            })

        return posts

    def _fetch_reddit_posts(self, subreddits, queries):
        """
        For each subreddit + query pair, call ScrapeCreators
        /v1/reddit/subreddit/search and collect posts.

        Falls back to global /v1/reddit/search when no subreddits are
        configured.
        """
        posts = [{'id': '1u0hln0', 'title': 'I am looking to buy computers for my office workers', 'body': '', 'url': 'https://www.reddit.com/r/Entrepreneur/comments/1u0hln0/iot_business_has_anyone_here_built_one/', 'subreddit': 'Entrepreneur', 'author': 'Draviddavid'}
                 ]
        try:
            headers = self._get_scrapecreators_headers()

            for subreddit in subreddits:
                subreddit = subreddit.strip()
                if not subreddit:
                    continue

                for query in queries:
                    try:

                        _logger.info(
                            "Fetching r/%s query='%s'",
                            subreddit,
                            query,
                        )

                        response = requests.get(
                            "https://api.scrapecreators.com/v1/reddit/subreddit/search",
                            headers=headers,
                            params={
                                "subreddit": subreddit,   # no "r/" prefix
                                "query": query,
                                "sort": "new",
                                "timeframe": "week",      # recent posts only
                            },
                            timeout=15,
                        )

                        _logger.info(
                            "Response %s for r/%s query='%s'",
                            response.status_code,
                            subreddit,
                            query,
                        )

                        if response.status_code != 200:
                            _logger.warning(
                                "Mentions to Leads: ScrapeCreators returned %d "
                                "for r/%s query '%s'",
                                response.status_code, subreddit, query,
                            )
                            continue

                        data = response.json()

                        _logger.info(
                            "Received %d posts",
                            len(data.get("posts", []))
                        )

                        parsed = self._parse_scrapecreators_posts(
                            data,
                            subreddit,
                        )
                        posts.extend(parsed)

                    except Exception as e:
                        _logger.error(
                            "Mentions to Leads: fetch failed for r/%s '%s': %s",
                            subreddit, query, e,
                        )

        except ValueError as e:
            # API key not configured
            _logger.error("Mentions to Leads: %s", e)

        return posts

    # ------------------------------------------------------------------
    # STEP 3 — Score post for buying intent
    # ------------------------------------------------------------------

    def _score_post(self, post, product_desc, target_customer):
        params = self.env['ir.config_parameter'].sudo()
        api_key = params.get_param('crm_mention_leads.gemini_api_key')

        if not api_key:
            return 50, "No Gemini key configured"

        prompt = f"""
You are a B2B sales qualification expert.

Our Product:
{product_desc}

Our Target Customer:
{target_customer}

Post Title:
{post['title']}

Post Body:
{post['body'][:500]}

Score from 0 to 100 where:

80-100 = Strong buying intent
60-79 = Moderate intent
40-59 = Weak intent
0-39 = Not relevant

Return ONLY JSON.

Example:
{{
  "score": 75,
  "reason": "User is actively comparing tools and mentions budget"
}}
"""

        try:
            content = self._gemini_generate(prompt, temperature=0.2)
            breakpoint()
            result = json.loads(content)
            return (
                int(result.get("score", 0)),
                result.get("reason", "")
            )
        except Exception as e:
            _logger.error(
                "Mentions to Leads: scoring failed: %s", e)
            return 0, f"Scoring error: {e}"

    # ------------------------------------------------------------------
    # STEP 4 — Create CRM lead
    # ------------------------------------------------------------------

    def _create_lead(self, post, score):
        breakpoint()
        source = self.env['utm.source'].search(
            [('name', '=', 'Reddit')], limit=1)
        if not source:
            source = self.env['utm.source'].create({'name': 'Reddit'})

        lead = self.env['crm.lead'].create({
            'name': f"Reddit Mention — {post['title'][:60]}",
            'description': (
                f"<b>Subreddit:</b> r/{post['subreddit']}<br/>"
                f"<b>Author:</b> u/{post['author']}<br/>"
                f"<b>Intent Score:</b> {score}/100<br/>"
                f"<b>URL:</b> <a href='{post['url']}'>{post['url']}</a><br/><br/>"
                f"{post['body'][:1000]}"
            ),
            'source_id': source.id,
            'type': 'opportunity',
        })
        return lead

    # ------------------------------------------------------------------
    # STEP 5 — Log the mention
    # ------------------------------------------------------------------

    def _log_mention(self, post, score, reason, lead=None):
        self.env['crm.mention.log'].create({
            'post_title': post['title'],
            'post_url': post['url'],
            'post_body': post['body'][:2000],
            'subreddit': post['subreddit'],
            'reddit_author': post['author'],
            'post_reddit_id': post['id'],
            'intent_score': score,
            'score_reason': reason,
            'lead_created': bool(lead),
            'lead_id': lead.id if lead else False,
        })
