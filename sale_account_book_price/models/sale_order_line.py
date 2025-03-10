from odoo import api ,fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    book_price = fields.Float(
        string="Book Price",
        compute="_compute_book_price",
        help="Computes the book price form product_id, product_uom, product_uom_qty"
    )

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_book_price(self):
        for line in self:
            if not line.product_id:
                line.book_price = 0.0
                continue

            pricelist = line.order_id.pricelist_id

            if pricelist:
                line.book_price = pricelist._get_product_price(
                    line.product_id,
                    line.product_uom_qty,
                    line.product_uom,
                )
            else:
                line.book_price = line.product_id.lst_price
