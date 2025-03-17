# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SignItemParty(models.Model):
    _inherit = 'sign.item.role'

    auth_method = fields.Selection(
        selection_add=[('aadhar_esign', 'Aadhaar e-Sign')],
        ondelete={'aadhar_esign': 'set default'}
    )
