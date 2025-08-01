# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ReceiptsLayout(models.TransientModel):
    _name = "receipts.layout"
    _description = "Custom Reciept Template"

    pos_config_id = fields.Many2one(
        "pos.config",
        string="Point of Sale",
        default=lambda self: self.env["pos.config"].browse(
            self.env.context.get("active_pos_config_id")
        ),
        required=True,
    )
    receipt_layout = fields.Selection(related="pos_config_id.receipt_layout", required=True)
    receipt_logo = fields.Binary(related="pos_config_id.receipt_logo")
    receipt_header = fields.Html(related="pos_config_id.receipt_header_html")
    receipt_footer = fields.Html(related="pos_config_id.receipt_footer_html")
    preview = fields.Html("_compute_receipt_preview")

    def receipt_layout_save(self):
        return {"type": "ir.actions.act_window_close"}

    @api.depends("receipt_layout", "receipt_header", "receipt_footer", "receipt_logo")
    def _compute_receipt_preview(self):
        for wizard in self:
            if wizard.pos_config_id:
                wizard.preview = wizard.env["ir.ui.view"]._render_template(
                    wizard._get_template(),
                    {
                        "receipt_header": wizard.receipt_header,
                        "receipt_footer": wizard.receipt_footer,
                        "receipt_logo": wizard.receipt_logo,
                    },
                )
            else:
                wizard.preview = False

    def _get_template(self):
        is_restaurant = self.pos_config_id.module_pos_restaurant
        if is_restaurant:
            base_module = "pos_receipt.report_restaurant_preview"
        else:
            base_module = "pos_receipt.report_receipts_wizard_preview"

        layout_templates = {
            "light": f"{base_module}_light",
            "boxes": f"{base_module}_boxes",
            "lined": f"{base_module}_lined",
        }

        return layout_templates.get(self.receipt_layout, layout_templates["light"])
