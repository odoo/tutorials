from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    book_price = fields.Float(
        string="Book Price",
        compute="_compute_book_price",
        readonly=True,
        help="Computed Book Price based on the product\'s list price and ordered quantity.",
    )

    @api.depends("product_id", "product_uom_qty")
    def _compute_book_price(self):
        for line in self:
            if line.product_id:
                line.book_price = line.product_id.lst_price * line.product_uom_qty
            else:
                line.book_price = 0.0   
