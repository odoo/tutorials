# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deposit_product_id = fields.Many2one(
        'product.product', string="Deposit Product",
        help="This product will be used to add deposits in the Rental Order.",
        domain="[('product_tmpl_id.rent_ok', '=', True)]",
        config_parameter="sale_renting.deposit_product_id"
    )
