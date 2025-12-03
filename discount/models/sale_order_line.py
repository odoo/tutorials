from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_discount_line = fields.Boolean(
        string="Is Discount Line",
        default=False,
        help="Indicates if this line is a discount line created by the discount wizard."
    )

    def unlink(self):
        orders = self.mapped('order_id')
        res = super().unlink()
        for order in orders:
            product_lines = order.order_line.filtered(lambda line: not line.is_discount_line)
            discount_lines = order.order_line.filtered(lambda line: line.is_discount_line)
            if not product_lines and discount_lines:
                discount_lines.unlink()
        return res
