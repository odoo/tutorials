from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_auto_send_invoice = fields.Boolean(string="Send invoices automatically")
    auto_send_invoice_days = fields.Integer(string="Days to wait")

    def set_values(self):
        super().set_values()
        param = self.env["ir.config_parameter"].sudo()
        param.set_param("auto_invoice_email.is_active", self.is_auto_send_invoice)
        param.set_param("auto_invoice_email.days", self.auto_send_invoice_days)

    @api.model
    def get_values(self):
        res = super().get_values()
        param = self.env["ir.config_parameter"].sudo()
        res.update({
            "is_auto_send_invoice": param.get_param("auto_invoice_email.is_active") == 'True',
            "auto_send_invoice_days": int(
                param.get_param("auto_invoice_email.days", default=0)
            )
        })
        return res
