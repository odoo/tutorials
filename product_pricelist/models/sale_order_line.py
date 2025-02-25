from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    book_price = fields.Float(
        string="Book Price",
        compute="_compute_book_price",
        store=True
    )

    @api.depends('product_id', 'product_uom_qty')
    def _compute_book_price(self):
        for record in self:
            if not record.product_id:
                record.book_price = 0.0
            else:
                record.book_price = record._get_pricelist_price() * record.product_uom_qty
