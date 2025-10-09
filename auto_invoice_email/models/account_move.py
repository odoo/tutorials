
from datetime import timedelta
from odoo import api, models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _cron_send_invoice_by_email(self):
        send_invoice_days = int(self.env["ir.config_parameter"].sudo().get_param("send_email_invoice_days"))

        target_invoice_date = fields.date.today() - timedelta(days=send_invoice_days)
        invoices = self.search([
            ('state', '=', 'posted'),
            ('invoice_date', '=', target_invoice_date),
            ('is_move_sent', '=', False)
        ])
        template = self.env.ref("account.email_template_edi_invoice")
        self.env['account.move.send']._generate_and_send_invoices(invoices, mail_template=template)
