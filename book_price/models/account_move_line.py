# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    book_price = fields.Float(
        string="Book Price",
        compute="_compute_book_price",
        store=True)

    @api.depends("product_id.lst_price", "quantity")
    def _compute_book_price(self):
        for record in self:
            record.book_price = record.product_id.lst_price * \
                record.quantity if record.product_id else 0.00
