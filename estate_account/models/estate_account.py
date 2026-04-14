from odoo import Command, models


class EstateAccount(models.Model):
    _inherit = 'estate.property'

    def action_property_sold(self):

        super().action_property_sold()

        self.env['account.move'].create([{
            'partner_id': self.salesperson_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                'name': '6% commision',
                'price_unit': self.selling_price * 0.06,
                'quantity': 1,
                }),
                Command.create({
                'name': 'Administrative fees',
                'price_unit': 100,
                'quantity': 1,
                })
            ]
        }])
