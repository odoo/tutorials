from odoo import fields, models, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    book_price = fields.Float(string='Book Price', compute='_compute_book_price')

    @api.depends('product_id', 'quantity', 'sale_line_ids')
    def _compute_book_price(self):
        for rec in self:
            if rec.product_id:
                pricelist = rec.sale_line_ids.order_id.pricelist_id
                if pricelist:
                    rec.book_price = pricelist._get_product_price(
                        rec.product_id, rec.quantity
                    )
                else:
                    rec.book_price = rec.product_id.lst_price
            else:
                rec.book_price = 0
