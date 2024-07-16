from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sold = fields.Boolean(string="Can be sold", config_parameter="estate.sold")
