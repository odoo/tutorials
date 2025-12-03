from odoo import models


class SaleOrderDiscount(models.TransientModel):
    _inherit = "sale.order.discount"

    def _prepare_discount_line_values(self, product, amount, taxes, description=None):
        self.ensure_one()
        vals = super()._prepare_discount_line_values(product, amount, taxes, description)
        vals['is_discount_line'] = True
        return vals
