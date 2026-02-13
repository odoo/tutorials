from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    discount_percentage = fields.Float(
        string="Discount Amount",
    )

    @api.model
    def _get_discount_product(self):
        return self.env["product.product"].search([("name", "=", "Discount")], limit=1)

    def _update_discount(self):
        discount_product = self._get_discount_product()
        discount_line = self.order_line.filtered(
            lambda l: l.product_id == discount_product
        )
        product_lines = self.order_line.filtered(
            lambda l: l.product_id != discount_product
        )

        # if not product_lines and discount_line:
        #     discount_line.unlink()
        #     return

        total = sum(product_lines.mapped("price_subtotal"))
        discount_amount = -(total * self.discount_percentage / 100.0)

        if discount_line:
            discount_line.write({"price_unit": discount_amount})

    def action_confirm(self):
        res = super().action_confirm()
        if self.amount_total <= 0:
            raise ValidationError(
                "Cannot confirm the sale order with zero total amount."
            )
        return res

#    if discount_line:
#         discount_line.write({
#             "price_unit": discount_amount,
#             "product_uom_qty": 1,
#         })
