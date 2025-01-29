from odoo import Command, models

class Property(models.Model):
    _inherit = 'estate.house'

    def sell_property(self):
        print("I am the child behavior")
        print(self.buyer_id)
        self.env["account.move"].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': f'Buying Property {self.name}',
                    'price_unit': 0.6*self.selling_price,
                    'quantity': 1
                })
            ]
        })
        return super().sell_property()
