# -*- coding: utf-8 -*-
from odoo import api, fields, models

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"
    
    @api.depends("product_id")
    def _compute_product_stock_quant_ids(self):
        """
        Computes stock quants related to the product, filtering only those:
        - Belonging to the same company
        - Located in internal locations
        - Having a positive quantity
        """
        for line in self:
            line.product_stock_quant_ids = line.product_id.stock_quant_ids.filtered(
                lambda q: (
                    q.company_id in self.env.companies
                    and q.location_id.usage == "internal"
                    and q.quantity > 0
                )
            )
