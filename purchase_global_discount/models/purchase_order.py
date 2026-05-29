from odoo import _, api, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.readonly
    def action_open_discount_wizard(self):
        self.ensure_one()
        return {
            'name': _("Discount"),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order.discount',
            'view_mode': 'form',
            'target': 'new',
        }
