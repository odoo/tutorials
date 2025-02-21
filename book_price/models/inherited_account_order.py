from odoo import api, fields, models


class InheritedAccountOrder(models.Model):
    _inherit = "account.move.line"

    book_price = fields.Float(string='Book Price',compute = "_compute_book_price")

    @api.depends("product_id","quantity")
    def _compute_book_price(self):
        for record in self:
            record.book_price = record.product_id.list_price * record.quantity
