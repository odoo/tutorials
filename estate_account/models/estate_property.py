from odoo import models, Command


class EstateAccount(models.Model):
    _inherit = 'estate.property'

    def action_sold_property(self):
        self.env['account.move'].create({
            "partner_id": self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    "name": "selling price",
                    "quantity": 1,
                    'price_unit': 0.6 * self.selling_price

                }),
                Command.create({
                    "name": "administrative fees",
                    "quantity": 1,
                    'price_unit': 100.0

                })
            ]
        })

        return super().action_sold_property()
