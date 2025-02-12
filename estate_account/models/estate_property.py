from odoo import Command, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold_status(self):
        self.env['account.move'].create({
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price
                }),
                Command.create({
                    'name': 'Extra Charge (6%)',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100
                })
            ]
        })
        return super(EstateProperty, self).action_set_sold_status()
