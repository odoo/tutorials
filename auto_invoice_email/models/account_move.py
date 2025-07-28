# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api
from datetime import datetime, timedelta


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _auto_send_invoices(self):
        # Using sudo to access system parameters that are not user-specific and may be restricted
        days = int(self.env["ir.config_parameter"].sudo().get_param("auto_invoice_email.days", default=0))
        if days <= 0:
            return

        target_date = datetime.today().date() - timedelta(days=days)
        invoices = self.search([("state", "=", "posted"), ("invoice_date", "=", target_date), ("move_type", "in", ("out_invoice", "out_refund"))])
        template = self.env.ref("account.email_template_edi_invoice")
        for invoice in invoices:
            template.with_context(force_send=True).send_mail(invoice.id, force_send=True)
            invoice.message_post(body="Invoice automatically sent by cron job.", message_type="comment")
