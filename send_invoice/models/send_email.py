
from odoo import models, fields
from datetime import timedelta


class SendEmail(models.Model):
    _inherit = "account.move"

    def _send_email_invoice(self):
        """
        Use sudo() to bypass access rights when reading system parameters.
        Using sudo ensures the method can always retrieve the configuration
        value regardless of the user's permissions.
        """
        hour = self.env['ir.config_parameter'].sudo().get_param('send_invoice.send_invoice_via_email')
        if not hour:
            return

        try:
            hour = int(hour)
        except ValueError:
            return

        target_date = fields.Datetime.now() - timedelta(hours=hour)
        invoices = self.search([
            ('invoice_date', '=', target_date),
            ('payment_state', '!=', 'paid'),
            ('state', '=', 'posted')
        ])
        template = self.env.ref('account.email_template_edi_invoice', raise_if_not_found=False)
        if not template:
            return

        for invoice in invoices:
            template.send_mail(invoice.id, force_send=True)
