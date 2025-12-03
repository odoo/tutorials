import re
from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line')
    def _onchange_recalculate_global_discount(self):
        discount_lines = self.env['sale.order.line']
        for line in self.order_line:
            if line._is_global_discount():
                discount_lines += line

        if not discount_lines:
            return

        product_lines = self.env['sale.order.line']
        for line in self.order_line:
            if not line._is_global_discount() and not line.is_downpayment:
                product_lines += line

        if not product_lines:
            self.order_line -= discount_lines
            return

        subtotal = 0
        for line in product_lines:
            subtotal += line.price_subtotal

        for discount_line in discount_lines:
            match = re.search(r"(\d+(?:\.\d+)?)%", discount_line.name)
            if match:
                percent = float(match.group(1))
                discount_line.price_unit = -(subtotal * percent / 100)
