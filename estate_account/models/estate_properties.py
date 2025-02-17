# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, models
from odoo.exceptions import UserError


class EstateProperties(models.Model):
    _inherit = 'estate.properties'

    def action_property_sold(self):
        _ = self.env._
        super().action_property_sold()
        journal = self.env['account.journal'].search(
            [('type', '=', 'sale')], limit=1)

        if not journal:
            raise UserError(
                _ ('No Sales Journal found. Please configure a Sales Journal.'))

        for record in self:
            values = {
                'partner_id': record.partner_id.id,
                'move_type': 'out_invoice',
                'journal_id': journal.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': record.name,
                        'price_unit': record.selling_price,
                        'quantity': 1,
                    }), Command.create({
                        'name': '"6%" of Property Sale Price',
                        'price_unit': record.selling_price*0.06,
                        'quantity': 1,
                    }), Command.create({
                        'name': 'Administrative Fees',
                        'price_unit': 100,
                        'quantity': 1,
                    })

                ]
            }
            self.env['account.move'].create(values)
