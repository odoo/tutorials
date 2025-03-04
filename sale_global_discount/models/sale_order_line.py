# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import Command, _, fields, models
from odoo.tools import float_repr


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_global_discount_line = fields.Boolean(default=False, help="Whether this order line is global discount line")

    def unlink(self):
        lines_to_delete = self
        discount_lines_to_remove = self._recalculate_global_discounts()
        if discount_lines_to_remove:
            lines_to_delete += discount_lines_to_remove
        return super(SaleOrderLine, lines_to_delete).unlink()

    def _recalculate_global_discounts(self):
        sale_order = self.order_id
        global_discount_percentage = sale_order.global_discount_percentage
        if not global_discount_percentage:
            return None
        discount_lines = sale_order.order_line.filtered(lambda l: l.is_global_discount_line) - self
        remaining_lines = sale_order.order_line - discount_lines - self
        if not remaining_lines:
            sale_order.global_discount_percentage = 0
            return discount_lines
        total_amount_per_tax_group = defaultdict(float)
        for line in remaining_lines:
            if line.product_uom_qty and line.price_unit:
                discounted_price = line.price_unit * (1 - (line.discount or 0.0) / 100)
                total_amount_per_tax_group[frozenset(line.tax_id.ids)] += discounted_price * line.product_uom_qty
        discount_dp = self.env['decimal.precision'].precision_get('Discount')
        discount_lines_to_keep = set()
        for tax_group, subtotal in total_amount_per_tax_group.items():
            discount_amount = -subtotal * global_discount_percentage
            matching_discount_line = discount_lines.filtered(lambda l: frozenset(l.tax_id.ids) == tax_group)
            if matching_discount_line:
                matching_discount_line.write({"price_unit": discount_amount})
                discount_lines_to_keep.add(matching_discount_line.id)
            else:
                discount_line = self.env["sale.order.line"].create({
                    "order_id": sale_order.id,
                    "product_id": discount_lines.product_id.id,
                    "sequence": 999,
                    "price_unit": discount_amount,
                    "tax_id": [Command.set(list(tax_group))],
                    "is_global_discount_line": True,
                    "name": _(
                        "Discount %(percent)s%% - On products with taxes: %(taxes)s",
                        percent=float_repr(global_discount_percentage * 100, discount_dp),
                        taxes=", ".join(self.env["account.tax"].browse(tax_group).mapped('name')),
                    )
                })
                discount_lines_to_keep.add(discount_line.id)
        return discount_lines.filtered(lambda l: l.id not in discount_lines_to_keep)
