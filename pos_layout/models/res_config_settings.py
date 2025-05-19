from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_disp_type = fields.Selection(
    related='pos_config_id.pos_disp_type',
    string="POS Receipt Layout"
    )

    def action_open_receipt_preview_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'POS Receipt Preview',
            'res_model': 'pos.receipt.preview.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.ids},
        }


class PosConfig(models.Model):
    _inherit = 'pos.config'

    pos_disp_type = fields.Selection([
        ('default', 'Default'),
        ('lined', 'Lined'),
        ('boxed', 'Boxed'),
    ], string="POS Recipt Layout")
