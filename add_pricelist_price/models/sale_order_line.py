from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    book_price = fields.Float(string="Book Price", compute='_compute_book_price', store=True)

    @api.depends('product_id', 'product_uom_qty', 'order_id.pricelist_id')
    def _compute_book_price(self):
        for line in self:
            if line.product_id and line.order_id.pricelist_id:
                price = line.order_id.pricelist_id._get_product_price(
                    product=line.product_id, 
                    quantity=line.product_uom_qty or 1.0
                )
                line.book_price = price if price else 0.0
            else:
                line.book_price = 0.0
