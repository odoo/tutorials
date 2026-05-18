from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    book_price = fields.Float(
        string="Book Price",
        compute="_compute_book_price",
        readonly=True
    )

    @api.depends("sale_line_ids.book_price")
    def _compute_book_price(self):
        for line in self:
            if line.sale_line_ids:
                line.book_price = line.sale_line_ids[0].book_price
            else:
                line.book_price = 0.0
