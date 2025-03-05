# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order'

    def _get_order_lines_to_report(self):
        return super()._get_order_lines_to_report().filtered(lambda line: bool(line.price_unit))
