from odoo import models,Command

class EstateProperty(models.Model):
    _inherit='estate.property'

    def action_sold(self):
        super().action_sold()
        journal = self.env['account.journal'].search([('name', '=', 'Customer Invoices')]).id
        values= {
            'journal_id': journal,
            'move_type': "out_invoice",
            'partner_id': self.buyer_id.id,
            'line_ids': [
                Command.create({
                    'name': self.name,
                    'price_unit': self.selling_price 
                }),
                Command.create({
                    'name': '6% Tax',
                    'price_unit': (0.6 * self.selling_price) 
                }),
                Command.create({
                    'name': 'Administrative fees',
                    'price_unit':100
                })
            ]
        }
        move = self.env['account.move'].create(values)
