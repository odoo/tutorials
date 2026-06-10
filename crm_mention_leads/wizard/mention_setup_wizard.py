from odoo import fields, models


class MentionSetupWizard(models.TransientModel):
    _name = 'crm.mention.setup.wizard'
    _description = 'Mentions to Leads — Setup Wizard'

    product_description = fields.Text(
        string="What does your company sell?",
        placeholder="e.g. HR software for small and medium businesses",
        required=True,
    )
    target_customer = fields.Text(
        string="Who are your ideal customers?",
        placeholder="e.g. HR managers at companies with 50-500 employees",
        required=True,
    )
    target_industries = fields.Char(
        string="Target Industries",
        placeholder="e.g. Manufacturing, Retail, Healthcare",
    )
    target_subreddits = fields.Char(
        string="Subreddits to Monitor (comma separated)",
        default="entrepreneur,smallbusiness,startups,humanresources",
        required=True,
    )

    def action_confirm(self):
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('crm_mention_leads.product_desc', self.product_description)
        params.set_param('crm_mention_leads.target_customer', self.target_customer)
        params.set_param('crm_mention_leads.target_industries', self.target_industries or '')
        params.set_param('crm_mention_leads.subreddits', self.target_subreddits)
        return {'type': 'ir.actions.act_window_close'}
