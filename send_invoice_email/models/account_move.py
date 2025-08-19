from odoo import fields, models
from datetime import timedelta


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _send_email_invoice(self):

        hour = self.env['ir.config_parameter'].sudo().get_param('send_invoice_email.send_invoice_by_email')

        if hour is None:
            return

        try:
            hour = int(hour)
        except ValueError:
            return

        target_date = fields.Datetime.now() - timedelta(hours=hour)

        invoices = self.search([
    ('invoice_date', '<=', target_date.date()),
    ('payment_state', '!=', 'paid'),
    ('state', '=', 'posted')
])

        template = self.env.ref('account.email_template_edi_invoice', raise_if_not_found=False)
        if not template:
            return

        for invoice in invoices:
            template.send_mail(invoice.id, force_send=True)
