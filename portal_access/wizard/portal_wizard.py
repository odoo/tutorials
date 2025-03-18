# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

perms = [
    'is_so_perm',
    'is_quotes_perm',
    'is_rfq_perm',
    'is_po_perm',
    'is_invoices_perm',
    'is_projects_perm',
    'is_tasks_perm'
]

class PortalWizardUser(models.TransientModel):
    _inherit = 'portal.wizard.user'

    perms_id = fields.Many2one(comodel_name='portal.wizard.user.perms', string="Permissions", ondelete='cascade')

    def action_open_perms(self):
        if not self.perms_id:
            self.perms_id = self.env['portal.wizard.user.perms'].create({'wizard_user_id': self.id})
        if self.user_id:
            for perm in perms:
                self.perms_id[perm] = self.user_id[perm]
        return {
            'name': "Portal Permissions",
            'type': 'ir.actions.act_window',
            'res_model': 'portal.wizard.user.perms',
            'view_mode': 'form',
            'res_id': self.perms_id.id,
            'target': 'new'
        }

    def action_grant_access(self):
        super().action_grant_access()
        return self.action_open_perms()

class PortalWizardUserPerms(models.TransientModel):
    _name = 'portal.wizard.user.perms'
    _description = "Manage Home Page Access"

    wizard_user_id = fields.Many2one(comodel_name='portal.wizard.user', string="User", required=True, ondelete='cascade')
    partner_id = fields.Many2one(comodel_name='res.partner', related='wizard_user_id.partner_id',
        string="Contact", required=True, readonly=True, ondelete='cascade')

    is_so_perm = fields.Boolean(string="Show Sales Orders", default=True)
    is_quotes_perm = fields.Boolean(string="Show Quotations", default=True)
    is_rfq_perm = fields.Boolean(string="Show Request for Quotation", default=True)
    is_po_perm = fields.Boolean(string="Show Purchase Orders", default=True)
    is_invoices_perm = fields.Boolean(string="Show Invoices & Bills", default=True)
    is_projects_perm = fields.Boolean(string="Show Projects", default=True)
    is_tasks_perm = fields.Boolean(string="Show Tasks", default=True)

    def action_save(self):
        for perm in perms:
            if self.wizard_user_id.user_id[perm] != self[perm]:
                self.wizard_user_id.user_id[perm] = self[perm]
        return self.wizard_user_id.action_refresh_modal()

    def action_cancel(self):
        return self.wizard_user_id.action_refresh_modal()
