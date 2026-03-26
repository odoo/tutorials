from odoo import models


class InheritedPurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_open_discount_wizard(self):
        self.ensure_one()
        return {
            "name": "Discount",
            "type": "ir.actions.act_window",
            "res_model": "purchase.order.discount",
            "view_mode": "form",
            "target": "new",
        }
