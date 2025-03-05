from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_estate_account = fields.Boolean("Enable Invoice")
    module_estate_auction = fields.Boolean("Automated Auction")
