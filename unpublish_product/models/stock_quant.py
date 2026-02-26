from odoo import models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def write(self, vals):
        res = super().write(vals)

        products = self.mapped("product_id.product_tmpl_id")
        products.check_and_unpublish()

        return res
