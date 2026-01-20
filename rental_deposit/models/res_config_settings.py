from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    deposit_management = fields.Boolean("Deposits" , config_parameter="sale_renting.deposit_management")
