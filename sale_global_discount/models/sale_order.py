# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, Command
from collections import defaultdict


class SaleOrder(models.Model):
    _inherit = "sale.order"

    has_global_discount = fields.Boolean(string="Has Global Discount",
        compute="_compute_has_global_discount", store=True)
    global_discount_percentage = fields.Float(string="Global Discount (%)", store=True)

    @api.depends("order_line", "order_line.product_id", "company_id.sale_discount_product_id")
    def _compute_has_global_discount(self):
        for order in self:
            discount_product = order.company_id.sale_discount_product_id
            if not discount_product:
                order.has_global_discount = False
                continue

            order.has_global_discount = bool(
                order.order_line.filtered(
                    lambda line: line.product_id.id == discount_product.id
                )
            )

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        for order in orders:
            if order.has_global_discount and order.global_discount_percentage:
                order._update_global_discount()

        return orders

    def write(self, vals):
        result = super().write(vals)
        if "order_line" in vals:
            for order in self:
                if order.has_global_discount and order.global_discount_percentage:
                    order._update_global_discount()
        return result

    def _get_discount_lines(self):
        """Return order lines that are discount lines"""
        self.ensure_one()
        discount_product = self.company_id.sale_discount_product_id
        if not discount_product:
            return self.env["sale.order.line"]

        return self.order_line.filtered(
            lambda line: line.product_id.id == discount_product.id
        )

    def _get_regular_lines(self):
        """Return order lines that are not discount lines"""
        self.ensure_one()
        discount_product = self.company_id.sale_discount_product_id
        if not discount_product:
            return self.order_line

        return self.order_line.filtered(
            lambda line: line.product_id.id != discount_product.id
        )

    def _update_global_discount(self):
        """Update discount lines based on current order lines"""
        self.ensure_one()
        regular_lines = self._get_regular_lines()
        discount_lines = self._get_discount_lines()
        if not regular_lines:
            if discount_lines:
                discount_lines.unlink()
            self.global_discount_percentage = 0
            return
        if discount_lines:
            discount_lines.unlink()
        self._create_global_discount_lines(self.global_discount_percentage / 100)

    def _create_global_discount_lines(self, discount_percentage):
        """Create discount lines based on current order lines and discount percentage"""
        self.ensure_one()
        discount_product = self.company_id.sale_discount_product_id
        if not discount_product:
            return False
        total_price_per_tax_groups = defaultdict(float)
        for line in self._get_regular_lines():
            if not line.product_uom_qty or not line.price_unit:
                continue
            total_price_per_tax_groups[line.tax_id] += (
                line.price_unit * line.product_uom_qty
            )
        if not total_price_per_tax_groups:
            return False
        vals_list = []
        if len(total_price_per_tax_groups) == 1:
            taxes = next(iter(total_price_per_tax_groups.keys()))
            subtotal = total_price_per_tax_groups[taxes]
            vals = {
                "order_id": self.id,
                "product_id": discount_product.id,
                "sequence": 999,
                "price_unit": -subtotal * discount_percentage,
                "tax_id": [Command.set(taxes.ids)],
                "name": f"Discount: {discount_percentage * 100}%",
                "product_uom_qty": 1.0,
                "product_uom": discount_product.uom_id.id,
            }
            vals_list.append(vals)
        else:
            for taxes, subtotal in total_price_per_tax_groups.items():
                vals = {
                    "order_id": self.id,
                    "product_id": discount_product.id,
                    "sequence": 999,
                    "price_unit": -subtotal * discount_percentage,
                    "tax_id": [Command.set(taxes.ids)],
                    "name": f"Discount: {discount_percentage * 100}% - On products with taxes: {', '.join(taxes.mapped('name'))}",
                    "product_uom_qty": 1.0,
                    "product_uom": discount_product.uom_id.id,
                }
                vals_list.append(vals)
        if not vals_list:
            return False
        lines = self.env["sale.order.line"].create(vals_list)
        return lines
