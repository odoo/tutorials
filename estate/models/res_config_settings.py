from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    check_action_sold = fields.Boolean(
        string="enable sold", config_parameter="estate.property_sold"
    )
