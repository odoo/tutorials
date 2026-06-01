import re
from odoo import _, api, fields, models
from odoo.tools import float_repr


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    global_discount_percentage = fields.Float()

    @api.onchange('order_line')
    def _onchange_update_global_discount(self):
        discount_lines = self.env['sale.order.line']
        product_lines = self.env['sale.order.line']

        for line in self.order_line:
            if line._is_global_discount():
                discount_lines += line
            if not line._is_global_discount():
                product_lines += line

        if not discount_lines:
            return

        if not product_lines:
            self.order_line -= discount_lines
            return

        subtotal = sum(product_lines.mapped('price_subtotal'))

        for discount_line in discount_lines:

            discount_dp = self.env['decimal.precision'].precision_get('Discount')
            origin_record = self.env['sale.order'].browse(self.id.origin)

            match = re.search(r"(\d+(?:\.\d+)?)", discount_line.name)
            discount_from_name = float(match.group(1)) if match else False

            if not discount_from_name:
                self.env.user._bus_send("simple_notification", {
                    'type': 'danger',
                    'title': _("Error"),
                    'message': _("Discounts should be in Float(0.00%)")
                })
                percent = origin_record.global_discount_percentage

                discount_line.name = _(
                    "Discount %(percent)s%%",
                    percent=float_repr(percent, discount_dp),
                )
                return

            if discount_from_name != self.global_discount_percentage:
                origin_record.global_discount_percentage = discount_from_name

            percent = origin_record.global_discount_percentage

            discount_line.name = _(
                "Discount %(percent)s%%",
                percent=float_repr(percent, discount_dp),
            )
            discount_line.price_unit = -(subtotal * (percent / 100))
