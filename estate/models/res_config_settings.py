from odoo import fields, models


class InheritConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    can_be_sold = fields.Boolean("Can Be Sold", config_parameter='estate.be_sold')
