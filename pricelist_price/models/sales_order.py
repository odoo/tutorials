from odoo import api, fields, models
from odoo.exceptions import UserError


class SalesOrder(models.Model):
    _inherit = 'sale.order.line'

    book_price = fields.Float(string="Book Price", compute="_compute_book_price", store= True)


    @api.depends("product_id", "order_id.pricelist_id", "product_uom_qty")
    def _compute_book_price(self):
        for record in self:
            pricelist = record.order_id.pricelist_id
            if pricelist and record.product_id:
                record.book_price = pricelist._get_product_price(record.product_id, record.product_uom_qty, record.order_id.partner_id)
            else:
                record.book_price = 0 

    @api.onchange('price_unit')
    def _check_book_price(self):
        for line in self:
            if line.book_price < line.price_unit * 0.8:
                return {
                    'warning': {
                        'title': "Price Warning",
                        'message': "The book price is significantly lower than the unit price!",
                    }
                }

    def _prepare_invoice_line(self, **kwargs):
            res = super()._prepare_invoice_line(**kwargs)
            res["book_price"] = self.book_price  
            return res
