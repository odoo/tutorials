from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    auto_unpublish_out_of_stock = fields.Boolean(
        string="Auto Unpublish Out-of-Stock Products",
        config_parameter="unpublish_product.auto_unpublish_out_of_stock",
    )
