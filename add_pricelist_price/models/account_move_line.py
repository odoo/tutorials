from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    book_price = fields.Float(string="Book Price", compute='_compute_book_price', store=True)

    @api.depends('product_id', 'quantity', 'move_id.invoice_origin', 'sale_line_ids')
    def _compute_book_price(self):
        for line in self:
            sale_order_line = line.sale_line_ids[:1]
            if sale_order_line and sale_order_line.order_id.pricelist_id:
                pricelist = sale_order_line.order_id.pricelist_id
                line.book_price = pricelist._get_product_price(
                    line.product_id, line.quantity
                )
            else:
                line.book_price = 0.0
