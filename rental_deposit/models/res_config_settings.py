from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    rental_deposit_product_id = fields.Many2one(
        'product.product',
        string='Deposit Product',
        domain=[('sale_ok', '=', True)],
        config_parameter='rental_deposit.product_id'
    )
