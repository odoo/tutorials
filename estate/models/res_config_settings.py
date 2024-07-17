from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sell_property = fields.Boolean("Sell Property", default=False, config_parameter="estate.sold")
