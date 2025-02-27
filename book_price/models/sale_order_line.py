# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    book_price = fields.Float(
        string="Book Price",
        compute="_compute_book_price",
        readonly=True,
        store=True)

    @api.depends("product_id", "product_uom_qty")
    def _compute_book_price(self):
        for record in self:
            if record.product_id:
                record.book_price = record.product_id.lst_price * record.product_uom_qty
            else:
                record.book_price = 0.00
