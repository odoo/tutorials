from odoo import fields, models


class resConfigSettingsView(models.TransientModel):
    _inherit = 'res.config.settings'

    module_stock_transport = fields.Boolean()
