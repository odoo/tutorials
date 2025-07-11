from odoo import models, fields, api


class PosReceiptLayout(models.TransientModel):
    _name = "pos.receipt.layout"
    _description = "Point of Sale Receipt Layout Configuration"

    pos_config_id = fields.Many2one(
        "pos.config",
        string="Point of Sale Configuration",
        default=lambda self: self.env["pos.config"].browse(
            self.env.context.get("active_pos_config_id")
        ),
        required=True,
    )

    receipt_layout = fields.Selection(
        related="pos_config_id.receipt_layout", readonly=False, required=True
    )
    receipt_logo = fields.Binary(related="pos_config_id.receipt_logo", readonly=False)
    receipt_header = fields.Text(related="pos_config_id.receipt_header", readonly=False)
    receipt_footer = fields.Text(related="pos_config_id.receipt_footer", readonly=False)
    is_restaurant = fields.Boolean(related="pos_config_id.module_pos_restaurant")
    receipt_preview = fields.Html(compute="_receipt_preview")

    @api.depends("receipt_layout", "receipt_header", "receipt_footer", "receipt_logo")
    def _receipt_preview(self):
        if self.receipt_layout == "light":
            self.receipt_preview = self.env["ir.ui.view"]._render_template(
                "pos_receipt.custom_receipt_light",
                {
                    "header": self.receipt_header,
                    "footer": self.receipt_footer,
                    "logo": self.receipt_logo,
                    "is_restaurant": self.is_restaurant,
                },
            )
        elif self.receipt_layout == "boxes":
            self.receipt_preview = self.env["ir.ui.view"]._render_template(
                "pos_receipt.custom_pos_receipt_boxed",
                {
                    "header": self.receipt_header,
                    "footer": self.receipt_footer,
                    "logo": self.receipt_logo,
                    "is_restaurant": self.is_restaurant,
                },
            )
        elif self.receipt_layout == "lined":
            self.receipt_preview = self.env["ir.ui.view"]._render_template(
                "pos_receipt.custom_receipt_lined",
                {
                    "header": self.receipt_header,
                    "footer": self.receipt_footer,
                    "logo": self.receipt_logo,
                    "is_restaurant": self.is_restaurant,
                },
            )

    def document_layout_save(self):
        return {"type": "ir.actions.act_window_close"}
