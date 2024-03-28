from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold_state(self):
        super().action_set_sold_state()
        return self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'line_ids': [
                Command.create(
                    {
                        'name': self.name,
                        'quantity': 1,
                        'price_unit': self.selling_price * 0.06
                    }
                ),
                Command.create(
                    {
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100
                    }
                )
            ]
        })
