# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _add_deposit_product(self, order_line):
        deposit_product_id = int(self.env['ir.config_parameter'].sudo().get_param('deposit_rental.deposit_product', default=0))
        if not deposit_product_id:
            raise UserError(_("This product requires a deposit, but no deposit item is configured. Please configure it in Rental Settings."))
        deposit_id = self.env['product.product'].browse(deposit_product_id)
        if not deposit_id.exists():
            raise UserError(_("The configured deposit product does not exist."))
        existing_deposit_line = self.order_line.filtered(lambda line: line.linked_line_id.id == order_line.id)
        if existing_deposit_line:
            existing_deposit_line.product_uom_qty = order_line.product_uom_qty
        else:
            self.env['sale.order.line'].create({
                'order_id': self.id,
                'product_id': deposit_product_id,
                'product_uom_qty': order_line.product_uom_qty,
                'product_uom': deposit_id.uom_id.id,
                'price_unit': deposit_id.list_price,
                'linked_line_id': order_line.id,
            })
