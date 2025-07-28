from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    book_price = fields.Float(string="Book Price", compute="_compute_book_price", store="true", readonly=True)

    @api.depends("product_id")
    def _compute_book_price(self):
        self.book_price = self.product_id.lst_price
