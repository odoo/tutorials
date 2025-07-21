# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    book_price = fields.Float(string="Book Price", compute="_compute_book_price", store=True)

    @api.depends("product_uom_qty", "product_id.lst_price")
    def _compute_book_price(self):
        for record in self:
            record.book_price = record.product_uom_qty * record.product_id.lst_price