# -*- coding: utf-8 -*-
from odoo import models, Command


class EstatePropertyAccount(models.Model):
    _inherit = 'estate_property'
    _description = 'Real Estate Property Account'

    def action_set_sold_property(self):
        self.env['account.move'].create({
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
            'journal_id': 1,
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price,
                }),
                Command.create({
                    'name': 'Administrations Fees',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
            ],
        })
        return super().action_set_sold_property()
