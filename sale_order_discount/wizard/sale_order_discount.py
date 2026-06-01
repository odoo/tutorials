from odoo import models


class SaleOrderDiscount(models.TransientModel):
    _inherit = 'sale.order.discount'

    def _prepare_global_discount_so_lines(self, base_lines):
        res = super()._prepare_global_discount_so_lines(base_lines)
        self.sale_order_id.global_discount_percentage = self.discount_percentage * 100
        return res
