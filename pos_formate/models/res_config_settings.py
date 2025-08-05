# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_receipt_layout = fields.Selection(
        selection=[
            ('light', 'Light'),
            ('boxed', 'Boxed'),
            ('lined', 'Lined'),
        ],
        string="POS Receipt Layout",
        default='light',
        config_parameter='pos.receipt.layout'
    )

    def action_open_receipt_configuration(self):
        """Open the wizard popup for receipt configuration"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Configure Receipt',
            'res_model': 'pos.configure.receipt',
            'view_mode': 'form',
            'target': 'new',
        }
