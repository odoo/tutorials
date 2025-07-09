from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    receipt_layout = fields.Selection(
        related="pos_config_id.receipt_layout", readonly=False
    )

    def open_pos_receipt_config_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Configure Receipt",
            "res_model": "pos.receipt.layout",
            "view_mode": "form",
            "target": "new",
            "context": {
                "active_pos_config_id": self.pos_config_id.id,
            },
        }
