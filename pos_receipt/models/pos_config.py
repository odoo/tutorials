# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class POSConfig(models.Model):
    _inherit = 'pos.config'

    receipt_layout = fields.Selection([
        ('light', 'Light'),
        ('lined', 'Lined'),
        ('boxes', 'Boxes'),
    ], string="Receipt Layout", default='light')

    receipt_logo = fields.Binary(string='Receipt Logo', related='company_id.logo', readonly=False)
