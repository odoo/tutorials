# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    book_price = fields.Float(string="Book Price", compute="_compute_book_price", store=True)

    @api.depends('product_id', 'product_uom_qty')
    def _compute_book_price(self):
        for line in self:
            if line.product_id and line.order_id.pricelist_id:
                line.book_price = line._get_pricelist_price()
            else:
                line.book_price = line.product_id.product_tmpl_id.list_price

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        res['book_price'] = self.book_price
        return res
