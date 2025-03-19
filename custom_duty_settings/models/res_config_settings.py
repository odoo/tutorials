from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_custom_duty_management = fields.Boolean(string="Import Export Settings")
