from odoo import models, Command


class InheritedModel(models.Model):
    _inherit = 'estate.property'

    def sold_button_action(self):

        for record in self:
            self.env['account.move'].create({
                'name': record.name,
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'line_ids': [
                    Command.create({
                        'name': '6% of the selling price',
                        'quantity': 1,
                        'price_unit': record.selling_price * .06
                    }),
                    Command.create({
                        'name': 'administrative fees',
                        'quantity': 1,
                        'price_unit': 100
                    })
                ],
            })

        return super().sold_button_action()
