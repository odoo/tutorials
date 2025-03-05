# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models

class SaleOrderDiscount(models.TransientModel):
    _inherit = 'sale.order.discount'

    @api.model
    def default_get(self, fields_list):
        """Reset manual discount removal flag when opening the discount wizard ONLY for 'Global Discount'."""
        res = super().default_get(fields_list)
        sale_order = self.env['sale.order'].browse(self.env.context.get('active_id'))

        if sale_order:
            discount_wizard = self.env['sale.order.discount'].search([
                ('sale_order_id', '=', sale_order.id),
                ('discount_type', '=', 'so_discount')
            ], limit=1)

            if discount_wizard:
                sale_order.global_discount_removed = False
                sale_order.global_discount_applied = True

        return res
