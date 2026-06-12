import json
import logging
import requests

from odoo import api, models

_logger = logging.getLogger(__name__)


class CrmMentionJob(models.TransientModel):
    _name = 'crm.mention.job'
    _description = 'Mention Lead Scanner'

    # ------------------------------------------------------------------
    # ENTRY POINT — called by cron
    # ------------------------------------------------------------------

    @api.model
    def run_mention_scan(self):
        params = self.env['ir.config_parameter'].sudo()

        if not params.get_param('crm_mention_leads.enabled'):
            _logger.info("Mentions to Leads: disabled, skipping scan.")
            return

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

        # Step 1 — Generate intent queries (1 Gemini call)
        queries = self._generate_intent_queries(product_desc, target_customer)
        _logger.info("Mentions to Leads: generated %d queries", len(queries))

        # Step 2 — Fetch Reddit posts
        posts = self._fetch_reddit_posts(subreddits.split(','), queries)

        # Deduplicate against already-processed posts
        new_posts = [
            p for p in posts
            if not self.env['crm.mention.log'].post_already_processed(p['id'])
        ]
        _logger.info("Mentions to Leads: %d new posts to score",
                     len(new_posts))

        if not new_posts:
            return

        # Step 3 — Score ALL posts in a single Gemini call
        scored = self._score_posts_batch(
            new_posts, product_desc, target_customer)

        # Step 4 — Split into leads_to_create and logs_to_write
        qualifying = [s for s in scored if s['score'] >= threshold]
        _logger.info("Mentions to Leads: %d posts qualify (score >= %d)", len(
            qualifying), threshold)

        # Bulk create leads — 1 DB call
        leads_by_post_id = self._create_leads_bulk(qualifying)

        # Bulk create logs — 1 DB call for all posts
        self._log_mentions_bulk(scored, leads_by_post_id)

        _logger.info(
            "Mentions to Leads: scan complete. %d leads created.", len(qualifying))

    # ------------------------------------------------------------------
    # STEP 1 — Generate intent queries (1 Gemini call)
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
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": temperature,
                    "responseMimeType": "application/json",
                },
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]

    def _generate_intent_queries(self, product_desc, target_customer):
        params = self.env['ir.config_parameter'].sudo()
        if not params.get_param('crm_mention_leads.gemini_api_key'):
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
  "payroll tool recommendation"
]
"""
        try:
            return json.loads(self._gemini_generate(prompt, temperature=0.7))
        except Exception as e:  # noqa: BLE001
            _logger.error("Mentions to Leads: query generation failed: %s", e)
            return [product_desc[:50]]

    # ------------------------------------------------------------------
    # STEP 2 — Fetch Reddit posts via ScrapeCreators
    # ------------------------------------------------------------------

    def _get_scrapecreators_headers(self):
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
        posts = []
        try:
            headers = self._get_scrapecreators_headers()
            for subreddit in subreddits:
                subreddit = subreddit.strip()
                if not subreddit:
                    continue
                for query in queries:
                    try:
                        _logger.info("Fetching r/%s query='%s'",
                                     subreddit, query)
                        response = requests.get(
                            "https://api.scrapecreators.com/v1/reddit/subreddit/search",
                            headers=headers,
                            params={
                                "subreddit": subreddit,
                                "query": query,
                                "sort": "new",
                                "timeframe": "week",
                            },
                            timeout=15,
                        )
                        if response.status_code != 200:
                            _logger.warning(
                                "Mentions to Leads: ScrapeCreators returned %d for r/%s query '%s'",
                                response.status_code, subreddit, query,
                            )
                            continue
                        data = response.json()
                        _logger.info("Received %d posts",
                                     len(data.get("posts", [])))
                        posts.extend(
                            self._parse_scrapecreators_posts(data, subreddit))
                    except Exception:  # noqa: BLE001
                        _logger.exception(
                            "Mentions to Leads: fetch failed for r/%s '%s'",
                            subreddit,
                            query,
                        )
        except ValueError as e:
            _logger.error("Mentions to Leads: %s", e)
        return posts

    # ------------------------------------------------------------------
    # STEP 3 — Score ALL posts in ONE Gemini call
    # ------------------------------------------------------------------

    def _score_posts_batch(self, posts, product_desc, target_customer):
        """
        Send all posts to Gemini in a single call.
        Returns the same list with 'score' and 'reason' added to each post.
        """
        params = self.env['ir.config_parameter'].sudo()
        if not params.get_param('crm_mention_leads.gemini_api_key'):
            # No AI key — assign default score to all
            return [{**p, 'score': 50, 'reason': 'No Gemini key configured'} for p in posts]

        # Build a numbered list of posts for the prompt
        posts_text = "\n\n".join(
            f"[{i}] Title: {p['title']}\nBody: {p['body'][:300]}"
            for i, p in enumerate(posts)
        )

        prompt = f"""
You are a B2B sales qualification expert.

Our Product:
{product_desc}

Our Target Customer:
{target_customer}

Score each post below for buying intent from 0 to 100 where:
80-100 = Strong buying intent
60-79 = Moderate intent
40-59 = Weak intent
0-39  = Not relevant

Posts:
{posts_text}

Return ONLY a JSON array with one object per post, in the same order.
Each object must have "index", "score", and "reason".

Example:
[
  {{"index": 0, "score": 75, "reason": "User is actively comparing tools"}},
  {{"index": 1, "score": 20, "reason": "Unrelated post about personal finance"}}
]
"""
        try:
            content = self._gemini_generate(prompt, temperature=0.2)
            results = json.loads(content)

            # Map scores back onto posts by index
            score_map = {r['index']: r for r in results}
            scored_posts = []
            for i, post in enumerate(posts):
                result = score_map.get(i, {})
                scored_posts.append({
                    **post,
                    'score': int(result.get('score', 0)),
                    'reason': result.get('reason', ''),
                })
            return scored_posts

        except Exception as e:  # noqa: BLE001
            _logger.error("Mentions to Leads: batch scoring failed: %s", e)
            # Fallback — assign 0 to all so nothing slips through
            return [{**p, 'score': 0, 'reason': f'Scoring error: {e}'} for p in posts]

    # ------------------------------------------------------------------
    # STEP 4 — Bulk create leads — 1 DB call
    # ------------------------------------------------------------------

    def _create_leads_bulk(self, qualifying_posts):
        """
        Create all qualifying leads in a single ORM create() call.
        Returns a dict of {post_id: lead_id} for logging.
        """
        if not qualifying_posts:
            return {}

        source = self.env['utm.source'].search(
            [('name', '=', 'Reddit')], limit=1)
        if not source:
            source = self.env['utm.source'].create({'name': 'Reddit'})

        vals_list = []
        for post in qualifying_posts:
            vals_list.append({
                'name': f"Reddit Mention — {post['title'][:60]}",
                'description': (
                    f"<b>Subreddit:</b> r/{post['subreddit']}<br/>"
                    f"<b>Author:</b> u/{post['author']}<br/>"
                    f"<b>Intent Score:</b> {post['score']}/100<br/>"
                    f"<b>URL:</b> <a href='{post['url']}'>{post['url']}</a><br/><br/>"
                    f"{post['body'][:1000]}"
                ),
                'source_id': source.id,
                'type': 'opportunity',
            })

        # Single DB call for all leads
        leads = self.env['crm.lead'].create(vals_list)

        # Map post_id → lead record for log linking
        return {
            post['id']: lead
            for post, lead in zip(qualifying_posts, leads)
        }

    # ------------------------------------------------------------------
    # STEP 5 — Bulk create logs — 1 DB call
    # ------------------------------------------------------------------

    def _log_mentions_bulk(self, scored_posts, leads_by_post_id):
        """
        Write all mention logs in a single ORM create() call.
        """
        if not scored_posts:
            return

        vals_list = []
        for post in scored_posts:
            lead = leads_by_post_id.get(post['id'])
            vals_list.append({
                'post_title': post['title'],
                'post_url': post['url'],
                'post_body': post['body'][:2000],
                'subreddit': post['subreddit'],
                'reddit_author': post['author'],
                'post_reddit_id': post['id'],
                'intent_score': post['score'],
                'score_reason': post['reason'],
                'lead_created': bool(lead),
                'lead_id': lead.id if lead else False,
            })

        # Single DB call for all logs
        self.env['crm.mention.log'].create(vals_list)
