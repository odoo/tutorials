from odoo import models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    receipt_layout = fields.Selection([
        ('light', 'Light'),
        ('boxes', 'Boxes'),
        ('lined', 'Lined')
    ], string='Receipt Layout', default='light')

    receipt_logo = fields.Binary(
        string='Receipt Logo', 
        default=lambda self: self.env.company.logo, 
        help='A logo that will be printed in the receipt.'
    )
    receipt_header = fields.Html(string='Header', default='', help="Custom HTML header for receipts")
    receipt_footer = fields.Html(string='Footer', default='', help="Custom HTML footer for receipts")
