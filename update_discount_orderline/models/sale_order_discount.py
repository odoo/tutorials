from odoo import models


class SaleOrderDiscount(models.TransientModel):
    _inherit = "sale.order.discount"

    def _prepare_discount_line_values(self, product, amount, taxes, description=None):
        res = super()._prepare_discount_line_values(product, amount, taxes, description)
        res["is_discount_line"] = True
        res["discount_precentage"] = self.discount_percentage * 100
        return res
