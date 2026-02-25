from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class PurchaseOrderDiscount(models.TransientModel):
    _name = "purchase.order.discount"
    _description = "Apply Global Discount on Purchase Order"

    discount = fields.Float(string="discount", required=True)
    discount_type = fields.Selection(
        [("amount", "$"), ("percent", "%")],
        default="percent",
        string="Discount Type",
        required=True,
    )
    discount_percent = fields.Float(
        compute="_calculate_percentage", string="Calculated Percentage"
    )
    order_id = fields.Many2one(
        "purchase.order",
        string="Purchase Order",
        required=True,
    )

    @api.constrains("discount", "discount_type")
    def _check_discount_limit(self):
        if (
            self.discount < 0 or self.discount > 100
        ) and self.discount_type == "percent":
            raise ValidationError("Discount value is invalid")

    def _get_base_untaxed_amount(self, order):
        total = 0.0
        for line in order.order_line:
            total += line.price_unit * line.product_qty
        return total

    @api.depends("discount", "discount_type")
    def _calculate_percentage(self):
        base_amount = self._get_base_untaxed_amount(self.order_id)
        if self.discount_type == "percent":
            self.discount_percent = self.discount
        elif base_amount > 0:
            self.discount_percent = (self.discount * 100) / base_amount
        else:
            self.discount_percent = 0

    def action_apply_discount(self):
        self.ensure_one()
        if not self.order_id.order_line:
            raise UserError("There are no lines on this order to discount.")

        base_amount = self._get_base_untaxed_amount(self.order_id)

        if self.discount_type == "percent":
            target_discount = self.discount
        else:
            if base_amount <= 0:
                raise UserError("Cannot apply an amount discount to a $0 order.")
            target_discount = (self.discount * 100) / base_amount

        # Final check to ensure calculated amount doesn't exceed 100%
        if target_discount > 100:
            raise UserError("The discount amount exceeds the total value of the order.")

        self.order_id.order_line.write({"discount": target_discount})
