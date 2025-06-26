from odoo import api, models
from datetime import date, timedelta


class AccountMove(models.Model):
    _inherit = "account.move"

    def _send_invoice_email(self):
        self.ensure_one()

        template = self.env.ref("account.email_template_edi_invoice")
        template.send_mail(self.id)
        self.message_post(body="Invoice automatically sent by cron job.")

    @api.model
    def method_to_send_invoice_automatically(self):
        automatic_send_invoice_days = int(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("invoice_send_automatic.automatic_send_invoice_days")
        )
        target_invoice_date = date.today() - timedelta(days=automatic_send_invoice_days)

        invoices_to_send = self.search(
            [
                ("state", "=", "posted"),
                ("move_type", "in", ("out_invoice", "out_refund")),
                ("invoice_date", "=", target_invoice_date),
            ]
        )
        for invoice in invoices_to_send:
            invoice._send_invoice_email()
