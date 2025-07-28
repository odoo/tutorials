# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date, timedelta
from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _cron_send_invoice_by_email(self):
        """
        Uses `sudo()` to securely access system configuration parameters.
        """
        send_invoice_days = int(self.env["ir.config_parameter"].sudo().get_param("send_email_invoice_days"))
        target_invoice_date = date.today() - timedelta(days=send_invoice_days)
        invoices = self.search([('state', '=', 'posted'), ('invoice_date', '=', target_invoice_date)])
        template = self.env.ref("account.email_template_edi_invoice")
        self.env['account.move.send']._generate_and_send_invoices(invoices, mail_template=template)
