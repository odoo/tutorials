from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    estate_property_sold = fields.Boolean(
        "Can be Sold", config_parameter="estate.property_sold"
    )
