from odoo import models, fields


class EstateConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    estate_account_invoicing = fields.Boolean(string="Invoicing", config_parameter='estate.enable_invoicing')
    estate_enable_auction_auto = fields.Boolean(
        string="Automated Auction",
        config_parameter='estate.enable_auction_auto'
    )
