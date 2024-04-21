from odoo import Command, models

class EstateProperty(models.Model):
    _inherit = "estate_property"

    def action_sold(self):
        self.ensure_one()
        invoice_vals = self._prepare_invoice()
        invoice_lines_vals = self._prepare_invoice_lines()
        invoice_vals['invoice_line_ids'] = [Command.create(invoice_line_id) for invoice_line_id in invoice_lines_vals]
        self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals)
        return super().action_sold()

    def _prepare_invoice(self):
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
        }
        return invoice_vals

    def _prepare_invoice_lines(self):
        """
        Prepare the list of values to create the new invoice lines.
        """
        return [
            {
                'name': self.name,
                'quantity': 1,
                'price_unit': 0.06 * self.selling_price,
            },
            {
                'name': "Adminstrative Fees",
                'quantity': 1,
                'price_unit': 100,
            },
        ]
