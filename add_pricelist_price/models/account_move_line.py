from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    book_price = fields.Float(
        string="Book Price",
        compute="_compute_book_price",
        readonly=True,
        help="Computed book price based on product list price and quantity.",
    )

    @api.depends("product_id", "quantity")
    def _compute_book_price(self):
        for line in self:
            if line.product_id:
                line.book_price = line.product_id.lst_price * line.quantity
            else:
                line.book_price = 0.0  
