# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_cashfree_esign = fields.Boolean(
        string="Sign With Aadhaar eSign",
        default=False,
        config_parameter='ESigner.esign_enabled',
    )

    cashfree_client_id = fields.Char('Cashfree Client ID', config_parameter='cashfree_client_id')
    cashfree_client_secret = fields.Char('Cashfree Client Secret', config_parameter='cashfree_client_secret')
