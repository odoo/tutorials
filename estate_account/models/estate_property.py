# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self.env['account.move'].create(
            {
                'partner_id': self.buyer.id,
                'move_type': 'out_invoice',
                "invoice_line_ids": [
                    Command.create({
                        'name': self.name,
                        'quantity': 1,
                        'price_unit': 0.06 * self.selling_price,
                    }),
                    Command.create({
                        'name': "Administrative Fees",
                        'quantity': 1,
                        'price_unit': 100,
                    }),
                ]
            }
        )
        return super().action_sold()
