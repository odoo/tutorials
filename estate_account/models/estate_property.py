# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def property_sold_action(self):
        self.env['account.move'].sudo().create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': '6% of the selling price',
                    'quantity': 1,
                    'price_unit': round(self.selling_price * 0.06, 2)
                }),
                Command.create({
                    'name': 'an additional 100.00 from administrative fees',
                    'quantity': 1,
                    'price_unit': '100.00'
                })
            ]
        })
        return super().property_sold_action()
