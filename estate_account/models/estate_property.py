from odoo import models, Command


class Property(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        res = super().action_set_sold()

        self.check_access('create')

        self.env['account.move'].sudo().create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06
                }),
                Command.create({
                    'name': 'administrative fees',
                    'quantity': 1,
                    'price_unit': 100
                })
            ]
        })
        return res
