from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    book_price = fields.Float(string='Book Price', compute='_compute_book_price')

    @api.depends('product_id', 'product_uom_qty', 'order_id.pricelist_id')
    def _compute_book_price(self):
        for rec in self:
            if not rec.product_id:
                rec.book_price = 0
                continue
            pricelist = rec.order_id.pricelist_id
            if rec.product_id and pricelist:
                rec.book_price = pricelist._get_product_price(
                    rec.product_id, rec.product_uom_qty
                )
            else:
                rec.book_price = rec.product_id.lst_price
