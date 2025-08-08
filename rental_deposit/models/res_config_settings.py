from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deposit_product_id = fields.Many2one(
        'product.product',
        string="Deposit Product",
        config_parameter='rental_deposit.deposit_product_id'
    )
