# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    pricelist_price_unit = fields.Float(string="Book Price", compute='_compute_pricelist_price_unit')

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_pricelist_price_unit(self):
        for line in self:
            if line.product_id:
                line.pricelist_price_unit = line._get_pricelist_price()
            else:
                line.pricelist_price_unit = 0.0

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        res['pricelist_price_unit'] = self.pricelist_price_unit
        return res
