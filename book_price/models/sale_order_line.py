from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    book_price = fields.Float(
        string="Book Price",
        compute="_compute_book_price",
        readonly=True,
        help="A relevant pricelist price based on currently selected pricelist, product and quantity.",
    )

    @api.depends("product_id", "pricelist_item_id", "product_uom_qty")
    def _compute_book_price(self):
        """Compute `book_price` based on the selected pricelist item, product, and quantity.
        - If no product is selected, set price to 0.
        - If no pricelist item exists, use the product's default sale price (`lst_price`).
        - Otherwise, compute the price using `_get_pricelist_price()` and multiply by quantity."""
        
        for record in self:
            if not record.product_id:
                record.book_price = 0.0
            elif not record.pricelist_item_id:
                record.book_price = record.product_id.lst_price * record.product_uom_qty
            else:
                record.book_price = record._get_pricelist_price() * record.product_uom_qty
