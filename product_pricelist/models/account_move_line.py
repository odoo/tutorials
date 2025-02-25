from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    book_price = fields.Float(
        string="Book Price",
        compute="_compute_book_price",
        store=True
    )

    @api.depends('product_id', 'quantity', 'move_id.invoice_origin')
    def _compute_book_price(self):
        pass
        #define
