# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models

class Property(models.Model):
    _inherit = "estate.property"

    def action_sell_the_property(self):

        move_val = {
            'move_type': 'out_invoice',
            'partner_id': self.property_buyer_id.id,
            'invoice_line_ids': [
                (0, 0, {
                    'name': self.name,
                    'quantity': 1.0,
                    'price_unit': self.selling_price 
                    }
                ), 
                (0, 0, {
                    'name': 'Commission',
                    'quantity': 1.0,
                    'price_unit': self.selling_price * 0.06
                    }
                ),
                (0, 0, {
                    'name': 'Administrative Fee',
                    'quantity': 1.0,
                    'price_unit': 100.00
                    }
                )
            ]
        }

        move = self.env['account.move'].create(move_val)

        return super().action_sell_the_property()
        