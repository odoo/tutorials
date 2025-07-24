# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    global_discount_percentage = fields.Float(string="Global Discount Percentage")

    def _remove_discount_if_needed(self):
        for order in self:
            order_lines = order.order_line
            product_lines = order_lines.filtered(lambda o: not o.is_global_discount)
            discount_lines = order_lines.filtered(lambda o: o.is_global_discount)
            if not product_lines:
                discount_lines.unlink()

    def _update_global_discount(self):
        for order in self:
            product_lines = order.order_line.filtered(lambda o: not o.is_global_discount)
            discount_line = order.order_line.filtered(lambda o: o.is_global_discount)

            if not discount_line:
                return

            subtotal = 0.0
            for line in product_lines:
                line_discount = (line.discount or 0.0) / 100.0
                discounted_price = line.price_unit * (1 - line_discount)
                subtotal += discounted_price * line.product_uom_qty

            discount_percentage = self.global_discount_percentage
            new_discount_amount = -1 * subtotal * discount_percentage
            discount_line.write({
                "price_unit": new_discount_amount,
                "name": f"Discount {discount_percentage * 100:.0f}%",
                })

    def write(self, vals):
        result = super().write(vals)
        if "order_line" in vals:
            self._remove_discount_if_needed()
            self._update_global_discount()
        return result
