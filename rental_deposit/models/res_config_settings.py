# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deposit_product = fields.Many2one(
        'product.product',
        string='Deposit Product',
        domain=lambda self: self._deposit_product_domain(),
        help='Product to be used for deposit on rental orders',
        config_parameter='rental.deposit_product',
    )

    @api.model
    def _deposit_product_domain(self):
        deposit_products = self.env['product.product'].search([('product_tmpl_id.name', '=', 'Deposit')])
        return [('id', 'in', deposit_products.ids)]
