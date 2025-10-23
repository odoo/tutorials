from odoo import models
from odoo import Command


class EstatePropertyAccount(models.Model):
    _inherit = 'estate.property'

    def sell_property(self):
        self.ensure_one()
        buyer = self.buyer_id
        invoice_values = {
            'move_type': 'out_invoice',
            'partner_id': buyer.id,
            'line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price
                }),
                Command.create({
                    'name': 'Taxes',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06
                }),
                Command.create({
                    'name': 'Administrative fees',
                    'quantity': 1,
                    'price_unit': 100.00
                })
            ]
        }
        self.env['account.move'].create(invoice_values)
        return super().sell_property()
