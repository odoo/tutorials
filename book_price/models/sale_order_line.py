# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    book_price = fields.Float(string='Book Price', compute="_compute_book_price")

    @api.depends("product_id", "order_id.pricelist_id", "product_uom_qty")
    def _compute_book_price(self):
        for line in self:
            if line.product_id and line.order_id.pricelist_id:
                price_unit = line.order_id.pricelist_id._get_product_price(
                    line.product_id, line.product_uom_qty, line.product_uom
                )
            else:
                price_unit = line.product_id.lst_price

            line.book_price = price_unit * line.product_uom_qty
