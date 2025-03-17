# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _update_purchase_order_line(self, product_id, product_qty, product_uom, company_id, values, line):
        res = super()._update_purchase_order_line(product_id, product_qty, product_uom, company_id, values, line)
        if line.sale_order_line_id:
            res["price_unit"] = line.sale_order_line_id.price_unit
        return res
