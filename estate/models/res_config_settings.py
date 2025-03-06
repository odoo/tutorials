from odoo import fields, models

    
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_estate_account = fields.Boolean(string="Enable Invoicing", default=False)
    module_estate_auction = fields.Boolean(string="Enable Auction", default=False)
