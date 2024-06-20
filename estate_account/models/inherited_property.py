# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _, Command

class InheritedProperty(models.Model):
    _inherit = "property"

    def action_set_state_sold(self):
        for real_estate in self :
            self.env['account.move'].create({
                    'partner_id' : real_estate.buyer_id.id,
                    'move_type':'out_invoice',
                    "line_ids": [ 
                    Command.create({'name': 'fixed rate', 'price_unit': real_estate.selling_price, 'quantity': 0.06}),
                    Command.create({'name': 'administrative fees', 'price_unit': 100, 'quantity': 1}),
                    ]  })
        return super().action_set_state_sold()