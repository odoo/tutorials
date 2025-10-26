from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    garden_area = fields.Integer(default=10, config_parameter="estate.default_garden_area")
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        config_parameter="estate.default_garden_orientation"
    )
