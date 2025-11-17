# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    sale_ids = fields.Many2many(
        "sale.order",
        "stock_picking_sale_order_rel", 
        "picking_id"
        "sale_id",  
        string="Sale Orders", 
    )

    new_return_ids = fields.Many2many("stock.picking", 
        "stock_picking_new_return_rel",
        "picking_id",
        "return_id",
        string="New Return Pickings",
    )

    @api.depends('return_ids', 'new_return_ids')
    def _compute_return_count(self):
        for picking in self:
            picking.return_count = len(set(picking.return_ids.ids) | set(picking.new_return_ids.ids))

    def action_see_returns(self):
        returns = self.return_ids | self.new_return_ids
        return {
            "name": _('Returns'),
            "type": "ir.actions.act_window",
            "res_model": "stock.picking",
            "view_mode": "list,form",
            "domain": [("id", "in", returns.ids)],
        }

    def _get_next_transfers(self):
        next_pickings = super()._get_next_transfers()
        return next_pickings.filtered(lambda p: p not in self.new_return_ids)

