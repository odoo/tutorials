from odoo import api, models, fields

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    book_price = fields.Float(string="Book Price",           
        compute='_compute_book_price', 
        default=0.0)

    @api.depends('product_id', 'quantity')
    def _compute_book_price(self):
        for line in self:
            pricelist = line.move_id.invoice_line_ids.sale_line_ids.order_id.pricelist_id
            if pricelist and line.product_id and line.quantity and line.product_uom_id:
                product_book_price = pricelist._get_product_price(
                    line.product_id,
                    line.quantity,
                    line.product_uom_id
                )
                line.book_price = product_book_price
            else:
                line.book_price = line.price_unit
