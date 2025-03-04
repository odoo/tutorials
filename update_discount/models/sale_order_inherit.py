from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    discount_percentage = fields.Float(string="Global Discount (%)")
    discount_wizard_ids = fields.One2many(
        "sale.order.discount", "sale_order_id", string="Discount Wizards"
    )

    def _add_or_update_discount(self):
        discount_product = self._get_discount_product()
        if not discount_product:
            return

        total_amount = sum(
            line.price_total for line in self.order_line if not line.is_discount_line()
        )

        if not total_amount:
            discount_lines = self.order_line.filtered(lambda l: l.is_discount_line())
            discount_lines.unlink()
            return

        if self.discount_wizard_ids:
            discount_percentage = self.discount_wizard_ids[-1].discount_percentage
        else:
            return

        discount_amount = total_amount * (discount_percentage)

        discount_line = self.order_line.filtered(lambda l: l.is_discount_line())

        if discount_line:
            discount_line.write(
                {
                    "price_unit": -discount_amount,
                    "name": "Discount ({:.2f}%)".format(discount_percentage * 100),
                    "product_uom_qty": 1,
                }
            )

    def _get_discount_product(self):
        """Fetch the predefined discount product"""
        return self.env["product.product"].search([("name", "=", "Discount")], limit=1)
