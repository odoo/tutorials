from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_estate_account = fields.Boolean('Enable Invoicing')

    module_estate_auction = fields.Boolean('Automated Auctions')
