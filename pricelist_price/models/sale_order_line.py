from odoo import api, models, fields


class SaleOrderLine(models.Model):
    _inherit = ['sale.order.line']

    book_price = fields.Float(
        string="Book Price",
        compute='_compute_book_price',)

    @api.depends('product_id', 'product_uom_qty', 'order_id.pricelist_id')
    def _compute_book_price(self):
        for line in self:
            line.book_price = 0.0
            pricelist = line.order_id.pricelist_id
            if pricelist and line.product_id and line.product_uom_qty and line.product_uom:
                product_book_price = pricelist._get_product_price(
                    line.product_id,
                    line.product_uom_qty,
                    line.product_uom
                )
                line.book_price = product_book_price
