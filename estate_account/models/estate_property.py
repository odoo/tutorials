# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.exceptions import AccessError
from odoo import Command, models

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold_property(self):
        for property in self:
            try:
                self.env['account.move'].check_access('create')
            except AccessError:
                raise AccessError("You do not have permission to sell this property.")

            self.env['account.move'].sudo().create({
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'line_ids': [
                    Command.create({
                        'name': "6% pf the selling price",
                        'quantity': len(property),
                        'price_unit': property.selling_price*0.06,
                    }),
                      Command.create({
                        'name': 'Administrative fees',
                        'quantity': len(property),
                        'price_unit': 100,
                    })
                ]
            })
        return super().action_sold_property()
