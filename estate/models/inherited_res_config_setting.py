from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_automated_real_estate_auction= fields.Boolean(string="Automated Auction", config_parameter='automated_auction.automated_auction')
    module_account = fields.Boolean(string="Enable Invoicing", config_parameter='stock.stock')
