# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, models

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):

        for record in self:
            self.env['account.move'].create({
                'partner_id': record.partner_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create(
                        {
                            'name': record.name,
                            'quantity': 1,
                            'price_unit': record.selling_price*0.6
                        }
                    ),
                    Command.create(
                        {
                            'name': 'Administratvive Fees',
                            'quantity': 1,
                            'price_unit': 100
                        }
                    )
                ]
            })

        return super().action_sold()
