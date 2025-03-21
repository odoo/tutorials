from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def updated_discount_amount(self):
        order_lines = self.order_line.filtered(lambda l: not l.is_discount_line)
        discount_line = self.order_line.filtered(lambda l: l.is_discount_line)
        total_amount = 0
        for line in order_lines:
            total_amount += line.price_subtotal
        return -(total_amount * (discount_line.discount_precentage / 100))
