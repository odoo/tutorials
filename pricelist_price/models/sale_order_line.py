from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    book_price = fields.Float(string="Book Price", readonly=True, compute="_compute_book_price")  # Remove compute

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_book_price(self):
        for record in self:
            if record.product_id:
                record.book_price = record._get_pricelist_price() * record.product_uom_qty
            else:
                record.book_price = 0.0
