# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, fields, models

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def set_property_sold(self):
        for record in self:
            record.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': record.buyer.id,
            'line_ids': [
                Command.create({
                    'name': record.name,
                    'quantity': 1,
                    'price_unit': record.selling_price * 0.06 + 100
                })
            ],
        })
        return super().set_property_sold()
