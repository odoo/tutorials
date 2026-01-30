from odoo import models, exceptions, Command


class EstateProperty(models.Model):
    _name = 'estate_property'
    _inherit = ['estate_property']

    def action_property_sold(self):

        if self.state != 'offer accepted':
            raise exceptions.UserError('An offer should be accepted')

        self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.buyer.id,
            'invoice_line_ids': [
                Command.create({
                    'name': 'Proportionnal fees',
                    'quantity': 0.06,
                    'price_unit': self.selling_price,
                }),
                Command.create({
                    'name': 'Administrative fees',
                    'quantity': 1.0,
                    'price_unit': 100.0,
                })
            ],
        })

        return super().action_property_sold()
