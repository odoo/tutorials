from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_open_discount_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Apply Discount",
            "res_model": "purchase.order.discount",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_purchase_order_id": self.id,
            },
        }
