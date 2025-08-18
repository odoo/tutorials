# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    receipt_layout = fields.Selection(related='pos_config_id.receipt_layout', readonly=False)

    def action_pos_receipt_layout(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Configure your pos receipt',
            'res_model': 'pos.receipt.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_pos_config_id': self.pos_config_id.id, 'dialog_size': 'extra-large'},
        }
