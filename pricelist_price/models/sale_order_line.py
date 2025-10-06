from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    book_price = fields.Float(string="Book Price", compute='_compute_book_price')

    @api.depends('product_id', 'product_uom_qty', 'order_id.pricelist_id')
    def _compute_book_price(self):
        pricelist = self.order_id.pricelist_id
        for line in self:
            pricelist = line.order_id.pricelist_id
            if pricelist and line.product_id and line.product_uom_qty and line.product_uom:
                line.book_price = pricelist._get_product_price(line.product_id,line.product_uom_qty,line.product_uom)
            else:
                line.book_price = 0.0
