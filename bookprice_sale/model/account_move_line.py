from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    book_price = fields.Float(string="Book Price", compute="_compute_book_price", store=True)

    @api.depends("quantity", "product_id.lst_price")
    def _compute_book_price(self):
        for record in self:
            if record.product_id:
                record.book_price = record.quantity * record.product_id.lst_price
            else:
                record.book_price = 0.0
