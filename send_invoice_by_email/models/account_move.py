from odoo import models, fields
from datetime import timedelta


# Extend account.move class to add cron method and custom email send methods
class AccountMove(models.Model):
    _inherit = 'account.move'

    # custom email send method
    def action_send_invoice_email_custom(self):
        for invoice in self:
            template = self.env.ref('account.email_template_edi_invoice', raise_if_not_found=False)
            if template:
                template.send_mail(invoice.id, force_send=True)

    # To check which invoice will sent today, call by ir.cron
    def cron_send_invoice_emails(self):
        param = self.env['ir.config_parameter'].sudo()
        days = param.get_param('send_invoice_by_email.send_email_days')

        if not days:
            return

        days = int(days)
        target_date = fields.Date.today() - timedelta(days=days)

        invoices = self.search([
            ('invoice_date', '=', target_date),
            ('state', '=', 'posted'),
        ])

        for invoice in invoices:
            invoice.action_send_invoice_email_custom()
