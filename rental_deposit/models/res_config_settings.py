from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deposit_product_id = fields.Many2one(
        'product.product',
        config_parameter="sale_renting.deposit_product_id"
    )
