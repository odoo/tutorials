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
    lead_id = fields.Many2one('crm.lead', string="Lead", readonly=True, ondelete='set null')

    # Meta
    fetched_on = fields.Datetime(string="Fetched On", default=fields.Datetime.now, readonly=True)
    post_reddit_id = fields.Char(string="Reddit Post ID", readonly=True)  # to avoid duplicate leads

    @api.model
    def post_already_processed(self, reddit_post_id):
        """Check if we already processed this Reddit post."""
        return self.search_count([('post_reddit_id', '=', reddit_post_id)]) > 0
