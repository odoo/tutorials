from odoo import models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def open_pos_receipt_config_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Configure Receipt",
            "res_model": "pos.config",
            "view_mode": "form",
            "target": "new",
        }
