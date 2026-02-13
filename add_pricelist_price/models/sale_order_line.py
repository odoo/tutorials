from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = ["sale.order.line"]

    book_price = fields.Monetary(compute="_compute_book_price", readonly=True)

    @api.depends('order_id.pricelist_id', 'product_id', 'product_uom_qty')
    def _compute_book_price(self):
        for line in self:
            if not line.product_id:
                line.book_price = 0
                continue
            pricelist = line.order_id.pricelist_id
            if line.product_id and pricelist:
                line.book_price = pricelist._get_product_price(
                    product=line.product_id,
                    quantity=line.product_uom_qty,
                )
            else:
                line.book_price = line.product_id.lst_price
