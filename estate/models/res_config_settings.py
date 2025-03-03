from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_estate_account = fields.Boolean(string="Invoice")
    module_automated_auction = fields.Boolean(string="Automated Auction")
