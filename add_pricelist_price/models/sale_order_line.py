from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    book_price = fields.Float(string="Book Price", compute='_compute_book_price', store=True)

    @api.depends('product_id', 'product_uom_qty', 'order_id.pricelist_id')
    def _compute_book_price(self):
        for line in self:
            if line.product_id and line.order_id.pricelist_id:
                line.book_price = line.order_id.pricelist_id._get_product_price(
                    line.product_id, 
                    line.product_uom_qty, 
                )
            else:
                line.book_price = 0.0
