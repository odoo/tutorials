from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    book_price = fields.Float(string="Book Price", compute='_compute_book_price', store=True)

    @api.depends('product_id', 'quantity', 'move_id.invoice_origin', 'sale_line_ids')
    def _compute_book_price(self):
        for line in self:
            if line.product_id and line.move_id and line.move_id.invoice_line_ids:
              product_pricelist = line.move_id.invoice_line_ids.mapped('sale_line_ids.order_id.pricelist_id')[:1]
              if product_pricelist:
                  price = product_pricelist._get_product_price(line.product_id, line.quantity or 1.0) or 0.0
                  line.book_price = price * (line.quantity or 1.0)
            else:
                line.book_price = 0.0
