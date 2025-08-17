from odoo import fields, models
from datetime import timedelta


class AccountMove(models.Model):
    _inherit = 'account.move'

    is_auto_email_sent = fields.Boolean(default=False)

    def _send_email_invoice(self):
        if not self.env['ir.config_parameter'].sudo().get_param('automatic_invoice.enable_auto_invoice_sending'):
            return

        try:
            days_str = self.env['ir.config_parameter'].sudo().get_param('automatic_invoice.invoice_send_delay_days')
            days = int(days_str)
        except ValueError:
            return

        target_date = fields.Datetime.now() - timedelta(days=days)
        invoices_to_send = self.search([
            ('state', '=', 'posted'),
            ('move_type', '=', 'out_invoice'),
            ('is_auto_email_sent', '=', False),
            ('invoice_date', '<=', target_date)
        ])

        template = self.env.ref('account.email_template_edi_invoice', raise_if_not_found=False)
        if not template:
            return

        for invoice in invoices_to_send:
            template.send_mail(invoice.id, force_send=True)
            invoice.is_auto_email_sent = True
