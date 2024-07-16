from odoo import fields, models


class EstateInheritModel(models.TransientModel):
    _inherit = "res.config.settings"

    sold = fields.Boolean(string="Sold", config_parameter="estate.sold")
