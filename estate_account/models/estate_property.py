from odoo import Command, models

class Property(models.Model):
    """
    Inherits from estate_property to extend the behavior of selling a property. The additional behavior
    is generating an invoice whenever a property is sold to a customer.
    """

    _inherit = "estate_property"

    def action_sold(self):
        """
        On selling a property, change its state to sold and create a customer invoice.
        A property cannot be sold if its advertisement is canceled or if it doesn't have an
        accepted offer.
        """
        self.ensure_one()
        self._create_account_move()
        return super().action_sold()

    def _create_account_move(self):
        invoice = self._prepare_invoice()
        invoice_lines = self._prepare_invoice_lines()
        invoice['invoice_line_ids'] = [Command.create(invoice_line) for invoice_line in invoice_lines]
        self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice)

    def _prepare_invoice(self):
        return {
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
        }

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
