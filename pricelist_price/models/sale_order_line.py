from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    book_price = fields.Float(
        string="Booked Price", 
        compute="_compute_book_price", 
    )

    @api.depends('product_id', 'order_id.pricelist_id', 'product_uom_qty')
    def _compute_book_price(self):
        for line in self:
            if line.order_id.pricelist_id and line.product_id:
                line.book_price = line.order_id.pricelist_id._get_product_price(
                    line.product_id, line.product_uom_qty, line.product_uom
                )
            else:
                line.book_price = 0.0
