from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    book_price = fields.Monetary(
        string="Book Price",
        related="sale_line_ids.book_price",
        store=True,
        readonly=True,
        help="Original book price fetched directly from the linked Sales Order line."
    )
