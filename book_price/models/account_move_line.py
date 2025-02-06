from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    book_price = fields.Float(string='Book Price', compute='_compute_book_price')

    @api.depends("product_id.lst_price" , "quantity")
    def _compute_book_price(self):
        for record in self:
            record.book_price = record.product_id.lst_price * record.quantity
