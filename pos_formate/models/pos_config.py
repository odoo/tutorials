from odoo import models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    receipt_layout = fields.Selection([
        ('light', 'Light'),
        ('boxed', 'Boxed'),
        ('lined', 'Lined'),
    ], string="Receipt Layout", default='light')

    receipt_logo = fields.Binary("Receipt Logo")
    receipt_header = fields.Text("Receipt Header")
    receipt_footer = fields.Text("Receipt Footer")
