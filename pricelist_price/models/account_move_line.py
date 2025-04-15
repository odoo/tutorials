from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    invoice_book_price = fields.Float(string="Book Price", compute="_compute_book_price", store=True, readonly=True)

    @api.depends("product_id")
    def _compute_book_price(self):
        self.invoice_book_price = self.product_id.lst_price
