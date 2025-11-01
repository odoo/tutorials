from odoo import fields, models


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    deposit_product_id = fields.Many2one('product.product', string='Deposit', config_parameter='deposit_in_rental_app.deposit_product_id')
