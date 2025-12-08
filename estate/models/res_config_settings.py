from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_estate_auction = fields.Boolean(
        string="Enable Auctions",
        help="Enable the auction feature for estate properties.",
        default=False,
    )
