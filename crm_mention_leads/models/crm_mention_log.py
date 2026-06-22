from odoo import api, fields, models


class CrmMentionLog(models.Model):
    _name = 'crm.mention.log'
    _description = 'Mention Scan Log'
    _order = 'fetched_on desc'

    # Post details
    post_title = fields.Char(string="Post Title", readonly=True)
    post_url = fields.Char(string="Post URL", readonly=True)
    post_body = fields.Text(string="Post Body", readonly=True)
    subreddit = fields.Char(string="Subreddit", readonly=True)
    reddit_author = fields.Char(string="Reddit Author", readonly=True)

    # Scoring
    intent_score = fields.Integer(string="Intent Score", readonly=True)
    score_reason = fields.Text(string="Score Reason", readonly=True)

    # Outcome
    lead_created = fields.Boolean(string="Lead Created", readonly=True)
    lead_id = fields.Many2one(
        'crm.lead', string="Lead", readonly=True, ondelete='set null')

    # Meta
    fetched_on = fields.Datetime(
        string="Fetched On", default=fields.Datetime.now, readonly=True)
    # to avoid duplicate leads
    post_reddit_id = fields.Char(string="Reddit Post ID", readonly=True)

    @api.model
    def _reddit_post_exists(self, reddit_post_id):
        return bool(
            self.search(
                [('post_reddit_id', '=', reddit_post_id)],
                limit=1,
            )
        )
