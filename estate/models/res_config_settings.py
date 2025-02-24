from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_estate_account = fields.Boolean(string="Invoicing", config_parameter='estate.use_invoicing')
