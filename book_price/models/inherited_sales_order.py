from odoo import api, fields, models


class InheritedSalesOrder(models.Model):
    _inherit = "sale.order.line"

    book_price = fields.Float(string='Book Price', compute='_compute_book_price')

    @api.depends("product_id.list_price" , "product_uom_qty")
    def _compute_book_price(self):
        for record in self:
            record.book_price = record.product_id.list_price * record.product_uom_qty
