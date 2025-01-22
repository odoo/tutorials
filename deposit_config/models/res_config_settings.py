from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_deposit_management = fields.Boolean("Deposit", default=False)
