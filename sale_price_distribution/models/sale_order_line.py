# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import  fields , models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    distributed_cost = fields.Float("Distributed Cost")

    def action_distribute_cost(self):
        self.write({})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Distribute Cost',
            'res_model': 'cost.distribution.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'order_id': self.order_id.id,
                'default_order_line_id': self.id,
                'default_price_subtotal': self.price_subtotal,
            }
        }
