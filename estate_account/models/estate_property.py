from odoo import models, Command
from odoo.exceptions import AccessError

class InheritedModel(models.Model):
    _inherit = "est.property"

    def sell_action(self):

        super().sell_action()
        
        self.env['account.move'].create({
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'line_ids':[
                Command.create({
                    'name': r'6% of the selling price',
                    'quantity': 1,
                    'price_unit': .06*self.selling_price,

                }),
                Command.create({
                    'name': 'Administrative fees',
                    'quantity': 1,
                    'price_unit': 100,
                })
            ]
        })