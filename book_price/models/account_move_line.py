from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    book_price = fields.Float(string="Book Price", compute="_compute_book_price")

    @api.depends("product_id.lst_price")
    def _compute_book_price(self):
        print(" Book Price ".center(100, "="))
        for record in self:
            print(record.move_type)
            print(record.product_id.lst_price)
            record.book_price = record.product_id.lst_price
