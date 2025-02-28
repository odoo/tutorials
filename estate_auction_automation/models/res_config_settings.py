from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_estate_auction_automation = fields.Boolean(
        string="Automated Auction",
        config_parameter='estate.use_auction_automation')
