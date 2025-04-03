# -*- coding: utf-8 -*-

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        for line in self:
            website_uom = line.product_id.website_uom_id
            if line.order_id.website_id and website_uom.category_id.name != "Unit":
                    line.product_uom = website_uom
        super()._compute_amount()
