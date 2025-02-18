# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, models
from odoo.exceptions import AccessError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self): # method for sold button
        for record in self:
            try:
                self.env['account.move'].check_access('create')
            except AccessError:
                raise AccessError("You do not have permission to sell this property.")

            self.env['account.move'].sudo().create({   #sudo() for bypass access rights and record rules.
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'line_ids': [
                    Command.create({
                        'name': '6% pf the selling price',
                        'quantity': len(record),
                        'price_unit': record.selling_price*0.06,
                    }),
                      Command.create({
                        'name': 'Administrative fees',
                        'quantity': len(record),
                        'price_unit': 100,
                    })
                ]
            })
        return super().action_sold_property()
