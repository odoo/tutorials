from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = ['estate.property']
    _name = 'estate.property'

    def action_sell(self):
        result = super().set_sell()

        for estate in self:
            self.env['account.move'].create({
                'partner_id': estate.buyer_id.id,
                'move_type':  'out_invoice',
                'line_ids': [
                    Command.create({
                        'name': self.env._("6% of the selling price"),
                        'quantity': 1,
                        'price_unit':  0.06 * estate.selling_price,
                    }),
                    Command.create({
                        'name': self.env._("administrative fee"),
                        'quantity': 1,
                        'price_unit':  100,
                    }),
                ]
            })

        return result
