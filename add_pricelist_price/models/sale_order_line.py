from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    book_price = fields.Float(string="Book Price", compute="_compute_book_price")

    @api.depends("product_id", "product_uom_qty", "order_id.pricelist_id")
    def _compute_book_price(self):
        for line in self:
            if line.product_id and line.order_id.pricelist_id:
                pricelist = line.order_id.pricelist_id
                product = line.product_id
                price = pricelist._get_product_price(
                    product,
                    quantity=line.product_uom_qty,
                    uom=line.product_uom,
                )
                line.book_price = price if price else line.product_id.lst_price
            else:
                line.book_price = line.product_id.lst_price
