from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Master toggle
    mention_leads_enabled = fields.Boolean(
        string="Mentions to Leads",
        config_parameter='crm_mention_leads.enabled',
    )

    # ScrapeCreators API key (replaces Reddit OAuth client_id/secret)
    scrapecreators_api_key = fields.Char(
        string="ScrapeCreators API Key",
        config_parameter='crm_mention_leads.scrapecreators_api_key',
    )

    # Gemini API key (for query generation + scoring)
    gemini_api_key = fields.Char(
        string="Gemini API Key",
        config_parameter='crm_mention_leads.gemini_api_key',
    )

    # Scoring threshold
    mention_score_threshold = fields.Integer(
        string="Minimum Intent Score (0-100)",
        config_parameter='crm_mention_leads.score_threshold',
        default=60,
    )

    def action_open_mention_setup_wizard(self):
        """Opens the setup wizard to configure company/customer profile."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Mentions to Leads — Setup',
            'res_model': 'crm.mention.setup.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
