# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    autosend_invoices = fields.Boolean(string="Send Invoice by Email")
    days_to_send_invoice = fields.Integer(string="Duration in days after the date of invoice.", default=0)

    @api.model
    def action_send_invoices_by_email(self):
        companies = self.env['res.company'].search([])
        for company in companies:
            if company.autosend_invoices:
                target_invoice_date = fields.Date.today() - relativedelta(days=company.days_to_send_invoice)
                if invoices := self.env['account.move'].search([
                        ('company_id', '=', company.id),
                        ('move_type', '=', 'out_invoice'),
                        ('state', '=', 'posted'),
                        ('invoice_date', '=', target_invoice_date),
                        ('is_move_sent', '=', False)
                    ]):
                    invoices.sending_data = {
                        'author_user_id': self.env.user.id,
                        'author_partner_id': self.env.user.partner_id.id,
                    }
        self.env.ref('account.ir_cron_account_move_send')._trigger()
        return True
