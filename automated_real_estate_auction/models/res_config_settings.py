from odoo import models, fields


class EstateConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_auction_auto = fields.Boolean(
        string="Automated Auction",
        config_parameter='estate.enable_auction_auto'
    )
