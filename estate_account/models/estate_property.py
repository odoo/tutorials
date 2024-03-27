from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold_state(self):
        super().action_set_sold_state()
        return self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            'line_ids': [
                Command.create({
                    'name': 'Adminstration fees',
                    'quantity': 1,
                    'price_unit': 100,
                }),
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                })
            ]
        })
