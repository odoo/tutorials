from odoo import models


class estateProperty(models.Model):
    _inherit = "estate.property"

    def action_estate_property_sold(self):
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        if journal:
            journal_id = journal.id
        else:
            journal_id = False
        invoice_vals = {
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
            'journal_id': journal_id,
        }
        new_invoice = self.env['account.move'].with_context(default_move_type='out_invoice').create(invoice_vals)
        invoice_vals_lines = []

        for prop in self:
            line1_vals = {
                'name': prop.name,
                'quantity': 1,
                'price_unit': prop.selling_price * 0.06
            }
            invoice_vals_lines.append((0, 0, line1_vals))

            line2_vals = {
                'name': 'Adminstrative Fee',
                'quantity': 1,
                'price_unit': 100.00
            }
            invoice_vals_lines.append((0, 0, line2_vals))

        new_invoice.write({'invoice_line_ids': invoice_vals_lines})
        return super().action_estate_property_sold()
