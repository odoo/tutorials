# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = ['sale.order.line']

    book_price = fields.Float(string="Book Price", compute="_compute_book_price",readonly=True, required=True, default=0.0)

    @api.depends('product_id', 'product_uom_qty')
    def _compute_book_price(self):
        for line in self:
            if not line.product_id:
                line.book_price = 0.0
            else:
                line.book_price = line._get_display_price()

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)

        for line in self:
            res.update({
                'book_price': line.book_price,
            })
        return res
