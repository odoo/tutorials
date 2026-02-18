from odoo import models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_purchase_global_discount(self):
        return {
            'name': 'Global Discount',
            'view_mode': 'form',
            'res_model': 'purchase.global.discount',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_order_id': self.id},
        }
