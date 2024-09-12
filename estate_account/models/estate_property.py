from odoo import fields, models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_mark_as_sold(self):
        print('Overrriden sold action')
        # selects the MISCELLANOUS journal
        # journal = self.env['account.move'].with_context(default_move_type='out_invoice')._search_default_journal()

        invoice_vals = {
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'journal_id': 1, # hardcoded Customer Invoices journal ID, ask for better way of doing this(?)
            "line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": self.selling_price
                }),
                Command.create({
                    "name": 'Administrative Tax',
                    "quantity": 1,
                    "price_unit": 100
                }),
                Command.create({
                    "name": '6% Tax',
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06
                })
            ],
        }

        moves = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals)

        return super().action_mark_as_sold()
