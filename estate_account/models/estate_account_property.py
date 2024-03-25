from odoo import models, Command
from odoo.exceptions import UserError


class EstateAccountProperty(models.Model):
    _inherit = 'estate.property'

    def action_mark_sold(self):
        if not self.buyer_id:
            raise UserError('No buyer yet, have you accepted an offer?')

        self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            'invoice_origin': self.name,
            'invoice_line_ids': [
                Command.create({
                    'name': f'6% down payment on {self.name}',
                    'quantity': 1,
                    'price_unit': 0.06 * self.selling_price,
                }),
                Command.create({
                    'name': 'Adminstrative Fees',
                    'quantity': 1,
                    'price_unit': 100.0,
                }),
            ]
        })
        return super().action_mark_sold()
