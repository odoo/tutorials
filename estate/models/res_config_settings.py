from odoo import models, fields
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_estate= fields.Boolean()
    module_auction_real_estate= fields.Boolean()
