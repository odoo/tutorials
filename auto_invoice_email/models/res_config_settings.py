# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    auto_send_invoice_days = fields.Integer(string="Send invoices after (days)")

    def set_values(self):
        super().set_values()
        self.env["ir.config_parameter"].sudo().set_param(
            "auto_invoice_email.days", self.auto_send_invoice_days
        )

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            {
                "auto_send_invoice_days": int(
                    self.env["ir.config_parameter"]
                    .sudo()
                    .get_param("auto_invoice_email.days", default=0)
                )
            }
        )
        return res
