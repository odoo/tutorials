# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deposit_product = fields.Many2one('product.product', string='Deposit')

    @api.model
    def get_values(self):
        res = super().get_values()
        deposit_product_id = self.env['ir.config_parameter'].sudo().get_param('deposit_rental.deposit_product', default=0)
        res.update(deposit_product=int(deposit_product_id) if deposit_product_id else False)
        return res

    def set_values(self):
        super().set_values()
        self.env['ir.config_parameter'].sudo().set_param('deposit_rental.deposit_product', self.deposit_product.id or False)
        self.env['product.template'].sudo()._update_deposit_amount()
