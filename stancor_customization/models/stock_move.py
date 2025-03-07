# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit="stock.move"

    s_quantity = fields.Float(
        string="S. Quantity",
        compute="_compute_s_quantity",
        related="sale_line_id.s_quantity",
        store=True
    )
    s_unit = fields.Selection(
        selection=[("kg", "Kg"),
                   ("mtrs", "Mtrs."),
                   ("pcs", "PCs."),],
        string="S. Unit",
        related="sale_line_id.s_unit",
        store=True
    )
    product_uom_qty = fields.Float(string="Quantity")

    @api.depends('product_uom_qty', 's_unit')
    def _compute_s_quantity(self):
        for move in self:
            wt_per_mt = move.sale_line_id.product_id.wt_per_mt or 1
            wt_per_pc = move.sale_line_id.product_id.wt_per_pc or 1
            
            if move.s_unit == 'mtrs':
                move.s_quantity = move.product_uom_qty / wt_per_mt
            elif move.s_unit == 'pcs':
                move.s_quantity = move.product_uom_qty / wt_per_pc
            else:  # 'kg'
                move.s_quantity = move.product_uom_qty / 1  

    def _create_backorder(self):
        res = super()._create_backorder()
        for backorder in res:
            backorder._compute_s_quantity()  
        return res

    def _action_done(self):
        if 'cancel_backorder' in self.env.context:
            self = self.with_context(cancel_backorder=None)

        res = super()._action_done()
        
        for move in self.filtered(lambda m: m.state == 'done' and m.sale_line_id):
            move.sale_line_id.qty_delivered += move.s_quantity
        
        return res