from odoo import api, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _cron_send_invoice_email(self): 
        invoices = self.search([
            ('state', '=', 'posted'),
            ('is_move_sent', '=', False),
            ('partner_id.email', '!=', False),
            ('move_type', 'in', self.get_sale_types())
        ])
        invoices.sending_data = {
            'author_user_id': self.env.user.id,
            'author_partner_id': self.env.user.partner_id.id,
        }
        if invoices:
            self.env['account.move.send']._generate_and_send_invoices(invoices, sending_methods=['email'], from_cron=True)
