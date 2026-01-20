# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        self._trigger_discount_update(lines)
        return lines

    def write(self, vals):
        result = super().write(vals)
        self._trigger_discount_update(self)
        return result

    def unlink(self):
        orders = self.mapped("order_id")
        result = super().unlink()
        for order in orders:
            if (
                order.exists()
                and order.has_global_discount
                and order.global_discount_percentage
            ):
                order._update_global_discount()
        return result

    def _trigger_discount_update(self, lines):
        """Trigger discount update for affected orders"""
        orders_to_update = self.env["sale.order"]
        for line in lines:
            if (line.product_id
                and line.order_id
                and line.order_id.company_id.sale_discount_product_id
                and line.product_id.id != line.order_id.company_id.sale_discount_product_id.id
                and line.order_id.has_global_discount
                and line.order_id.global_discount_percentage
            ):
                orders_to_update |= line.order_id

        for order in orders_to_update:
            order._update_global_discount()
