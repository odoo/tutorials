from odoo import api, fields, models


class EstateAccountPrice(models.Model):
    _inherit = 'account.move.line'
    _description = "Invoicing Book Price"
    book_price = fields.Monetary(compute="_compute_book_price", readonly=True)

    @api.depends('sale_line_ids.book_price')
    def _compute_book_price(self):
        for rec in self:
            if rec.sale_line_ids:
                rec.book_price = rec.sale_line_ids[0].book_price
            else:
                rec.book_price = 0.0
