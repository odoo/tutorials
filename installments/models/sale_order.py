from odoo import models,fields, api, Command

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    max_duration_setting = fields.Boolean(string="Is Warranty Available", default=False)
    def action_open_add_emi_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'New Wizard',
            'res_model': 'your.model.name',
            'view_mode': 'form',
            'target': 'new',
        }
