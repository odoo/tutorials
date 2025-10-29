# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    wizard_ids = fields.One2many(
        "sale.order.discount", "sale_order_id", string="Discount Wizards"
    )

    def _update_discount(self):
        discount_product = self.env["product.product"].search([("name", "=", "Discount")], limit=1)
        if not discount_product:
            return

        total_amount = sum(line.price_subtotal for line in self.order_line if not line.is_discount_line())
        discount_lines = self.order_line.filtered(lambda l: l.is_discount_line())
        if not total_amount:
            discount_lines.unlink()
            return

        if self.wizard_ids and discount_lines:
            discount_percentage = self.wizard_ids[-1].discount_percentage
        else:
            discount_lines.unlink()
            return

        discount_amount = total_amount * discount_percentage
        if len(discount_lines) > 1:
            discount_lines[1:].unlink()
            discount_line = discount_lines[0]
        elif discount_lines:
            discount_line = discount_lines[0]
        else:
            discount_line = False

        vals = {
            "price_unit": -discount_amount,
            "name": f"Discount {discount_percentage * 100:.2f}%",
        }

        if discount_line:
            discount_line.write(vals)
