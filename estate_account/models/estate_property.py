from odoo import Command, models
from odoo.exceptions import UserError


class EstatePropert(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        for property in self:
            if not property.buyer_id:
                raise UserError('Cannot create invoice: the property has no buyer.')
            move_vals = {
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'line_ids': [
                    Command.create({
                        'name': 'Selling price 6%',
                        'quantity': 1,
                        'price_unit': self.selling_price * 0.6
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100000
                    })
                ]
            }
            self.env['account.move'].create(move_vals)
        return super().action_set_sold()
