from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    discount_type = fields.Selection(
        selection=[
            ("value", "$"),
            ("percentage", "%"),
        ],
        default="percentage",
    )
    discount_in_value = fields.Float(string="Discount")
    discount_in_percentage = fields.Float(compute="_compute_discount_percentage", store=True, readonly=True)

    @api.depends("discount_type", "discount_in_value")
    def _compute_discount_percentage(self):
        for record in self:
            if record.discount_type == "value" and record.amount_total > 0:
                record.discount_in_percentage = (record.discount_in_value * 100) / (record.amount_total)
            elif record.discount_type == "percentage":
                record.discount_in_percentage = record.discount_in_value
            else:
                record.discount_in_percentage = 0.0

    @api.constrains("discount_in_value", "discount_type", "amount_total")
    def _check_discount_price(self):
        for record in self:
            if record.discount_type == "percentage":
                if record.discount_in_value < 0 or record.discount_in_value > 100:
                    raise ValidationError("discount value is not valid please check again")
            if record.discount_type == "value":
                if record.discount_in_value < 0 or record.discount_in_value > record.amount_total:
                    raise ValidationError("discount value is not valid please check again")

    def apply_discount(self):
        self.order_line.discount = self.discount_in_percentage

    def action_discount(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("Discount"),
            "res_model": "purchase.order",
            "view_mode": "form",
            "view_id": self.env.ref(
                "purchase_discount.view_purchase_order_discount_form"
            ).id,
            "res_id": self.id,
            "target": "new",
        }
