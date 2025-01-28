from odoo import Command, models
from odoo.exceptions import AccessError
import logging


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        sold_properties_success = super().action_sold()

        if not self.env['account.move'].check_access('create'):
            try:
                self.check_access('write')
                self.check_access_rule('write')
            except AccessError:
                logging.getLogger(__name__).warning(
                    'Could not create invoices from sold property')
                return sold_properties_success

        invoice_vals_list = []

        journal_id = self.env['account.journal'].search([
            ('code', '=', 'INV'),
            ('company_id', '=', self.env.company.id)
        ]).id

        for prop in self:
            invoice_vals = {
                'partner_id': prop.buyer_id.id,
                'move_type': 'out_invoice',
                'journal_id': journal_id,
                'line_ids': [
                    Command.create({
                        'name': f'{prop.name} #{prop.id}',
                        'quantity': 1,
                        'price_unit': prop.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative fee',
                        'quantity': 1,
                        'price_unit': 100.0,
                    })
                ]
            }
            invoice_vals_list.append(invoice_vals)

        self.env['account.move'].sudo().with_context(
            default_move_type='out_invoice').create(invoice_vals_list)

        return sold_properties_success
