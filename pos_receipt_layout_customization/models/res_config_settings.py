from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    receipt_layout = fields.Selection(
        related='pos_config_id.receipt_layout', readonly=False
    )

    def action_open_receipt_layout_wizard(self):
        return {
            'name': 'Configure Receipt Layout',
            'type': 'ir.actions.act_window',
            'res_model': 'pos.receipt.layout.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_pos_config_id': self.pos_config_id.id,
            }
        }
