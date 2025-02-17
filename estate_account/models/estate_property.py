# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, exceptions, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        print(self)
        journal = self.env['account.journal'].search(
            [('type', '=', 'sale')], limit=1)

        if not journal:
            raise exceptions.UserError(
                'No Sales Journal found. Please configure a Sales Journal.')

        for record in self:

            self.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'journal_id': journal.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': record.name,
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.6
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': '100.00'
                    })
                ]
            })

        return super().action_sold()
