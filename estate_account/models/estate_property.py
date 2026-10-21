# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, Command

class EstateProperty(models.Model):
    _inherit = 'estate_property'
    _description = 'Estate Property'

    def action_sold_estate_property(self):
        new_account_move = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            'invoice_line_ids': [Command.create({
                'name': self.name,
                'quantity': 1,
                'price_unit': self.selling_price,
            }),
            Command.create({
                'name': "Commission",
                'quantity': 1,
                'price_unit': self.selling_price * 0.06,
            }),
            Command.create({
                'name': "Administrative Fees",
                'quantity': 1,
                'price_unit': 100.0,
            }),
            ],
        })
        
        return super().action_sold_estate_property()