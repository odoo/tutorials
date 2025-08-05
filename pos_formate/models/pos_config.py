from odoo import models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    receipt_layout = fields.Selection([
        ('light', 'Light'),
        ('boxed', 'Boxed'),
        ('lined', 'Lined'),
    ], string="Receipt Layout", default='light')
