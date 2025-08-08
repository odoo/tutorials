from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    book_price = fields.Float(
        "Book Price", compute="_compute_book_price",
    )

    @api.depends("pricelist_item_id")
    def _compute_book_price(self):
        for line in self:
            if line.pricelist_item_id:
                line.book_price = (
                    line.pricelist_item_id.fixed_price * line.product_uom_qty
                )
            else:
                line.book_price = 0
