# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    book_price = fields.Float(string="Book Price", compute='_compute_book_price', store=True)

    @api.depends('product_id', 'product_uom_qty', 'order_id.pricelist_id', 'product_uom')
    def _compute_book_price(self):
        for line in self:
            if line.product_id and line.order_id.pricelist_id:
                price, _ = line.order_id.pricelist_id._get_product_price_rule(
                    line.product_id,
                    line.product_uom_qty,
                    uom = line.product_uom,
                )
                line.book_price = price  
            else:
                line.book_price = 0.0

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        res['book_price'] = self.book_price
        return res
