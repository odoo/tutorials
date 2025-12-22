# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class SaleOrderDiscount(models.TransientModel):
    _inherit = 'sale.order.discount'

    def _prepare_discount_line_values(self, product, amount, taxes, description=None):
        vals = super()._prepare_discount_line_values(product, amount, taxes, description)
        vals["is_global_discount"] = True
        self.sale_order_id.global_discount_percentage = self.discount_percentage
        return vals
