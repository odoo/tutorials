from odoo import fields, models


class PortalWizardUser(models.TransientModel):
    _inherit = 'portal.wizard.user'

    user_id = fields.Many2one('res.users', string='User')
    sales_order = fields.Boolean(related='user_id.portal_access_so', readonly=False)
    quotetion = fields.Boolean(related='user_id.portal_access_quotes', readonly=False)
    rfq = fields.Boolean(related='user_id.portal_access_rfq', readonly=False)
    purchase_order = fields.Boolean(related='user_id.portal_access_po', readonly=False)
    invoices = fields.Boolean(related='user_id.portal_access_invoices', readonly=False)
    projects = fields.Boolean(related='user_id.portal_access_projects', readonly=False)
    tasks = fields.Boolean(related='user_id.portal_access_tasks', readonly=False)

    def action_grant_access(self):
        super().action_grant_access()
        if self.user_id:
            self.user_id.update_portal_access_groups()
        return self.wizard_id._action_open_modal()
