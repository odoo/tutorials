from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    book_price = fields.Float(
        string="Book Price", compute="_compute_book_price"
    )

    @api.depends("product_id", "order_id.pricelist_id", "product_uom_qty")
    def _compute_book_price(self):
        for line in self:
            pricelist = line.order_id.pricelist_id
            if pricelist and line.product_id:
                book_price = pricelist._get_product_price(
                    line.product_id, line.product_uom_qty, line.product_uom
                )
                line.book_price = book_price
            else:
                line.book_price = 0.0
