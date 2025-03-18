# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _compute_picking_ids(self):
        for order in self:
            order.delivery_count = self.env["stock.picking"].search_count(
                ["|", ("sale_ids", "in", order.ids), ("sale_id", "=", order.id)]
            )

    def action_view_delivery(self):
        self.ensure_one()
        pickings = self.env["stock.picking"].search(
            ["|", ("sale_ids", "in", self.ids), ("sale_id", "=", self.id)],
        )
        return {
            "type": "ir.actions.act_window",
            "name": "Delivery Orders",
            "res_model": "stock.picking",
            "view_mode": "list,form",
            "domain": [("id", "in", pickings.ids)],
        }
