from odoo import Command, models


class Property(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()

        values = {
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'line_ids': [
                Command.create({
                    'name': '6% of the selling price',
                    'quantity': '1',
                    'price_unit': self.selling_price * 0.06
                }),
                Command.create({
                    'name': 'Administrative fees',
                    'quantity': '1',
                    'price_unit': 100
                })
            ]
        }
        self.env['account.move'].create(values)
        return res
