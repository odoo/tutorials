# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_deposit_line = fields.Boolean(string='Is Deposit Line', default=False)

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            product_id = val.get('product_id')

            if product_id:
                product = self.env['product.product'].browse(product_id)

                if product.product_tmpl_id.rent_ok and product.require_deposit:
                    deposit_product_id = int(self.env['ir.config_parameter'].sudo().get_param('rental.deposit_product', default=0))

                    if not deposit_product_id:
                        raise UserError(_("No deposit product configured. Please configure it in Rental Settings."))

                    deposit_product = self.env['product.product'].browse(deposit_product_id)
                    if not deposit_product.exists():
                        raise UserError(_("The configured deposit product does not exist anymore."))

                    sale_order_line = super().create([val])
                    deposit_line = {
                        'order_id': sale_order_line.order_id.id,
                        'product_id': deposit_product_id,
                        'name': f"Deposit for {product.product_tmpl_id.name}",
                        'product_uom_qty': sale_order_line.product_uom_qty,
                        'price_unit': product.deposit_amount,
                        'linked_line_id': sale_order_line.id,
                        'is_deposit_line': True
                    }
                    self.create(deposit_line)
                    return sale_order_line
                return super().create(vals_list)

    def write(self, vals):
        res = super().write(vals)
        for line in self:
            if 'product_uom_qty' in vals:
                deposit_line = self.env['sale.order.line'].search([('linked_line_id', '=', line.id)])
                if deposit_line:
                    deposit_line.write({'price_unit': line.product_id.deposit_amount*vals['product_uom_qty']})
                    deposit_line.write({'product_uom_qty': 1})

        return res
