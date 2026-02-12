from odoo import models, fields, api
from odoo.exceptions import UserError


class PurchaseOrderDiscount(models.TransientModel):
    _name = "purchase.order.discount"
    _description = "apply global discount on purchase order"

    discount = fields.Float()
    discount_type = fields.Selection(
        [("amount", "$"), ("percent", "%")], default="percent"
    )
    discount_percent = fields.Float(compute="_calculate_percentage")

    @api.depends("discount", "discount_type")
    def _calculate_percentage(self):
        order = self.env["purchase.order"].browse(self.env.context.get("active_id"))
        if self.discount_type == "percent":
            self.discount_percent = self.discount
        elif order.amount_untaxed != 0:
            self.discount_percent = (self.discount * 100) / order.amount_untaxed
        else:
            self.discount_percent = 0

    def action_apply_discount(self):
        order = self.env["purchase.order"].browse(self.env.context.get("active_id"))
        if self.discount_type == "percent":
            order.order_line.write({"discount": self.discount})
        elif order.amount_untaxed != 0:
            order.order_line.write({"discount": 0})
            self.discount = (self.discount * 100) / order.amount_untaxed
            order.order_line.write({"discount": self.discount})
        else:
            raise UserError(
                ("Cannot apply fixed discount because Total Amount is already zero.")
            )
