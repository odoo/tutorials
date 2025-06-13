# -*- coding: utf-8 -*-

from odoo import _, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _add_deposit_product(self, order_line):
        deposit_product_id = int(self.env['ir.config_parameter'].sudo().get_param('rental.deposit_product_id', default=0))
        if not deposit_product_id:
            raise UserError(_("No deposit product configured. Please configure it in Rental Settings."))

        deposit_product = self.env['product.product'].browse(deposit_product_id)
        if not deposit_product.exists():
            raise UserError(_("The configured deposit product does not exist anymore."))

        deposit_amount = order_line.product_id.deposit_amount * order_line.product_uom_qty
        existing_deposit_line = self.order_line.filtered(lambda l: l.linked_line_id.id == order_line.id)
        if existing_deposit_line:
            existing_deposit_line.product_uom_qty = 1
            existing_deposit_line.price_unit = deposit_amount
        else:
            self.env['sale.order.line'].create({
                'order_id': self.id,
                'product_id': deposit_product_id,
                'product_uom_qty': 1,
                'product_uom': deposit_product.uom_id.id,
                'price_unit': deposit_amount,
                'linked_line_id': order_line.id,
                'is_deposit_line': True
            })
