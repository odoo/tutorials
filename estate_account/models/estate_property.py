from odoo import Command, models


class InheritedEstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sell(self):
        res = super().action_sell()

        self.env['account.move'].create({
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'line_ids': [
                Command.create({
                    'name': '6% of the selling price',
                    'quantity': 1,
                    'price_unit': 0.06 * self.selling_price,
                }),
                Command.create({'name': 'Administrative fees', 'quantity': 1, 'price_unit': 100.0}),
            ],
        })

        return res
