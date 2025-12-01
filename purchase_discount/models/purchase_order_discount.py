from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PurchaseOrderDiscount(models.Model):
    _name = "purchase.order.discount"
    _description = "Purchase Order Discount"

    order_id = fields.One2many("purchase.order", "discount_id")
    discount_type = fields.Selection(
        selection=[
            ("value", "$"),
            ("percentage", "%"),
        ],
        default="value",
    )
    discount_in_value = fields.Float(string="Discount")
    discount_in_percentage = fields.Float(compute="_compute_discount_percentage", store=True, readonly=True)
    order_line_id = fields.Many2one("purchase.order.line")

    @api.depends("discount_type", "discount_in_value", "order_id.amount_total")
    def _compute_discount_percentage(self):
        for record in self:
            if record.discount_type == "value" and record.order_id.amount_total > 0:
                record.discount_in_percentage = (record.discount_in_value * 100) / (record.order_id.amount_total)
            elif record.discount_type == "percentage":
                record.discount_in_percentage = record.discount_in_value
            else:
                record.discount_in_percentage = 0.0

    @api.constrains("discount_in_value", "discount_type", "order_id.amount_total")
    def _check_discount_price(self):
        for record in self:
            if record.discount_type == "percentage":
                if record.discount_in_value < 0 or record.discount_in_value > 100:
                    raise ValidationError("discount value is not valid please check again")
            if record.discount_type == "value":
                if record.discount_in_value < 0 or record.discount_in_value > record.order_id.amount_total:
                    raise ValidationError("discount value is not valid please check again")

    def apply_discount(self):
        self.order_id.order_line.discount = self.discount_in_percentage

    def apply_cancle(self):
        pass
