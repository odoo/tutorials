from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        self.env['account.move'].create(
            {
                'partner_id': self.buyer_id.id,
                'move_type': 'out_invoice',
                'line_ids': [
                    Command.create({
                        'name': 'Deposit',
                        'quantity': '1',
                        'price_unit': 0.06 * self.selling_price,
                    }),
                    Command.create({
                        'name': 'Adminstrative fees',
                        'quantity': '1',
                        'price_unit': 100.0,
                    })
                ]
            }
        )
        return super().action_set_sold()
