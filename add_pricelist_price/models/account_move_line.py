from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    book_price = fields.Float(string="Book Price", related='sale_line_ids.book_price', readonly=True)
