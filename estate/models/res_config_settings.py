from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    selling_property = fields.Boolean(string="can we sold", config_parameter="estate.sold")
