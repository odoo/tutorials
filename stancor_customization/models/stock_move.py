# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit="stock.move"

    s_quantity = fields.Float(
        string="S. Quantity",
        compute="_compute_s_quantity",
        store=True
    )
    s_unit = fields.Selection(
        related="sale_line_id.s_unit",
        store=True
    )
    quantity = fields.Float(string="Quantity")

    @api.depends('quantity', 's_unit', 'sale_line_id.product_id.wt_per_mt', 'sale_line_id.product_id.wt_per_pc')
    def _compute_s_quantity(self):
        for move in self:
            move.s_quantity = 0
            product = move.sale_line_id.product_id if move.sale_line_id else move.product_id
            if product:
                wt_per_mt = product.wt_per_mt or 1
                wt_per_pc = product.wt_per_pc or 1
                unit_multipliers = {
                    "mtrs": wt_per_mt,
                    "pcs": wt_per_pc,
                    "kg": 1
                }
                move.s_quantity = move.quantity / unit_multipliers.get(move.s_unit, 1)

    def _create_backorder(self):
        backorders = super()._create_backorder()
        for backorder in backorders:
            backorder._compute_s_quantity()
        return backorders

    def _update_qty_delivered(self):
        for move in self.filtered(lambda m: m.state == 'done' and m.sale_line_id):
            move.sale_line_id.qty_delivered = move.quantity  

    def _action_done(self, **kwargs):
        res = super()._action_done(**kwargs)
        self._update_qty_delivered()
        return res
