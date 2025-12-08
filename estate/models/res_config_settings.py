from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_estate_account = fields.Boolean(string="Auto Install Estate Account")
    module_estate_auction = fields.Boolean(string="Auto Install Estate Auction")
