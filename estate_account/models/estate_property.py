from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sell(self):
        super().action_sell()

        self.env['account.move'].create(
            {
                'partner_id': self.partner_id.id,
                'move_type': 'out_invoice',
                'line_ids': [
                    Command.create(
                        {
                            'name': 'down payment',
                            'quantity': 1,
                            'price_unit': self.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {'name': 'administrative fees', 'quantity': 1, 'price_unit': 100}
                    ),
                ],
            }
        )

        return True
