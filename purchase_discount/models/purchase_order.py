from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    discount_id = fields.Many2one("purchase.order.discount")

    def action_discount(self):
        if not self.discount_id:
            new_data = self.env["purchase.order.discount"].create(
                {
                    "discount_type": "value",
                    "discount_in_value": 0,
                    "discount_in_percentage": 0,
                }
            )
            self.discount_id = new_data.id
        return {
            "type": "ir.actions.act_window",
            "name": "Discount",
            "res_model": "purchase.order.discount",
            "view_mode": "form",
            "view_id": self.env.ref(
                "purchase_discount.purchase_order_discount_view_form"
            ).id,
            "res_id": self.discount_id.id,
            "target": "new",
        }
