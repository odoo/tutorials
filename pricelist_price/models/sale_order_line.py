from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    book_price = fields.Float(string="Book Price", compute='_compute_book_price')

    @api.depends('product_id', 'product_uom_qty', 'order_id.pricelist_id')
    def _compute_book_price(self):
        for record in self:
            if not record.product_id:
                record.book_price = 0.0
                continue

            pricelist = record.order_id.pricelist_id if record.order_id else None

            if pricelist:
                record.book_price = pricelist._get_product_price(
                    record.product_id, record.product_uom_qty
                )
            else:
                record.book_price = record.product_id.lst_price
