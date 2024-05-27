from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        self.env['account.move'].create(
            {
                'partner_id': self.partner_id,
                'move_type': 'out_invoice',
                'line_ids': [
                    Command.create(
                        {
                            'name': 'Commission',
                            'quantity': 1,
                            'price_unit': 0.06
                            * self.offer_ids.filtered(lambda o: o.status == 'accepted').price,
                        }
                    ),
                    Command.create(
                        {
                            'name': 'Administrative fee',
                            'quantity': 1,
                            'price_unit': 100,
                        }
                    ),
                ],
            }
        )

        return super().action_sold()
