from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_estate_account = fields.Boolean(string="Enable Invoicing")
    module_estate_auction_automation = fields.Boolean(string="Automated Auction")
