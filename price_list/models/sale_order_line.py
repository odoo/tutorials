from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _description = "Sale order line inherit for price list"

    book_price = fields.Float(string = "Book Price", compute = "_compute_book_price")

    @api.depends("product_id", "order_id.pricelist_id", "product_uom_qty")
    def _compute_book_price(self):
        for line in self:
            pricelist = line.order_id.pricelist_id
            product = line.product_id
            quantity = line.product_uom_qty
            unit_of_measure = line.product_uom

            if pricelist and line.product_id:
                line.book_price = pricelist._get_product_price(product, quantity, unit_of_measure) 
            else:
                line.book_price = line.product_id.list_price
