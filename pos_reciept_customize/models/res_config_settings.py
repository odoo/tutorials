# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_receipt_layout = fields.Selection(related="pos_config_id.receipt_layout", readonly=False)

    def action_view_receipt_layout(self):
        return {
          "type": "ir.actions.act_window",
          "name": ("Configure your pos receipt"),
          "res_model": "receipts.layout",
          "view_mode": "form",
          "target": "main",
          "context": {"active_pos_config_id": self.pos_config_id.id, "dialog_size": "extra-large"},
        }
