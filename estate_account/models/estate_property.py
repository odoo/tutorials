from odoo import models, Command


class EstatePropertyTag(models.Model):
    _name = 'estate.property'
    _inherit = 'estate.property'

    def action_set_sold(self):
        # Search for the (account) journal to be used on the invoice
        journal = self.env['account.journal'].search(
            domain=[('type', '=', 'sale')])

        # Create a new invoice with the buyer_id.id, the journal.id and the type
        self.env['account.move'].create(
            {
                'partner_id': self.buyer_id.id,
                'invoice_user_id': self.salesperson_id.id,
                'move_type': 'out_invoice',
                'journal_id': journal.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': f'Partial payment for: {self.name}',
                        'quantity': 1,
                        'price_unit': self.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative fields',
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ]
            }
        )

        # Call the parent action
        return super().action_set_sold()
