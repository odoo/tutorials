# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deposit_product_id = fields.Many2one(
        'product.product',
        string='Deposit Product',
        help='Product to be used for deposit on rental orders',
        config_parameter='rental.deposit_product_id',
    )
