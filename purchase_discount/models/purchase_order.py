from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_purchase_global_discount(self):
        self.ensure_one()
        return {
            "name": "Discount",
            "type": "ir.actions.act_window",
            "res_model": "purchase.order.discount",
            "view_mode": "form",
            "target": "new",
        }
