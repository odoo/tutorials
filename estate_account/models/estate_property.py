from odoo import fields, models


class EstatePropertyAccount(models.Model):
    _inherit = "estate.property"

    invoice_id = fields.Many2one('account.move', string="Invoice")

    def action_estate_property_sold(self):

        # checking access rights
        self.check_access_rights('write')
        self.check_access_rule('write')

        journal = self.env['account.journal'].sudo().search([('type', '=', 'sale')], limit=1)
        if journal:
            journal_id = journal.id
        else:
            journal_id = False
        invoice_vals = {
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
            'journal_id': journal_id,
        }
        new_invoice = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals)
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

        new_invoice.sudo().write({'invoice_line_ids': invoice_vals_lines})
        return super().action_estate_property_sold()
