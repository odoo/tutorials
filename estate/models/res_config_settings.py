from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # sold = fields.Boolean()
    sold = fields.Boolean(string="Sold", config_parameter='estate.sold')
