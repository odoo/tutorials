# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    linked_line_id = fields.Many2one(
        'sale.order.line',
        string='Linked Order Line',
        help="Link to the order line this deposit is for"
    )
    is_deposit_line = fields.Boolean(string='Checks whether order line is deposit or not', default=False)

    @api.model_create_multi
    def create(self, vals):
        line = super().create(vals)
        if line.product_id.rent_ok and line.product_id.require_deposit:
            line.order_id._add_deposit_product(line)
        return line

    def write(self, vals):
        result = super().write(vals)
        if 'product_uom_qty' in vals:
            for line in self:
                if line.product_id.rent_ok and line.product_id.require_deposit:
                    line.order_id._add_deposit_product(line)
        return result
