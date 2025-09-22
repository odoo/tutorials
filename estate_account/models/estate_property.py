from odoo import Command, models
from odoo.exceptions import AccessError

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        if not self.env['account.move'].check_access('create'):
            try:
                self.check_access('write')
            except AccessError:
                return self.env['account.move']

        partner_id = self.buyer_id
        journal = self.env['account.journal'].search([
                *self.env['account.journal']._check_company_domain(self.env.company),
                ('type', '=', 'sale')], limit=1)
        property_name = self.name

        invoice_vals = {'partner_id': partner_id.id,
                        'move_type': 'out_invoice',
                        'journal_id': journal.id,
                        'invoice_line_ids': [
                            Command.create({
                                'name': property_name,
                                'quantity': 1,
                                'price_unit': self.selling_price * 6 / 100
                                }),
                            Command.create({
                                'name': "Administrative fees",
                                'quantity': 1,
                                'price_unit': 100
                                })
                            ]}

        self.env['account.move'].sudo().with_context(
                default_move_type='out_invoice').create(invoice_vals)

        return super().action_sold()
