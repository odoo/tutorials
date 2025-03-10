# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    deposit_require = fields.Boolean(string='Require Deposit')
    deposit_amount = fields.Float(string='Amount', compute='_compute_deposit_amount', store=True)

    @api.model
    def _update_deposit_amount(self):
        products = self.search([('deposit_require', '=', True)])
        products._compute_deposit_amount()

    @api.depends('deposit_require')
    def _compute_deposit_amount(self):
        deposit_product_id = self.env['ir.config_parameter'].sudo().get_param('deposit_rental.deposit_product')
        deposit_id = self.env['product.product'].sudo().search([('id', '=', int(deposit_product_id))]) if deposit_product_id else None

        for record in self:
            if record.deposit_require and deposit_id and deposit_id.exists():
                record.deposit_amount = deposit_id.list_price
            else:
                record.deposit_amount = 0.0
