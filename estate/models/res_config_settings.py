from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_estate_account = fields.Boolean(string="Enable Innvoicing")
    module_estate_auction = fields.Boolean(string="Automated Auction")
