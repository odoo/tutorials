# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StockQaunt(models.Model):
    _inherit="stock.quant"

    quantity_mtr = fields.Float(
        string="Quantity (MTR)",
        compute="_compute_quantities",
        store=True
    )
    quantity_pcs = fields.Float(
        string="Quantity (PCS)",
        compute="_compute_quantities",
        store=True
    )

    @api.depends('inventory_quantity_auto_apply', 'product_id.wt_per_mt', 'product_id.wt_per_pc')
    def _compute_quantities(self):
        for quant in self:
            wt_per_mt = quant.product_id.wt_per_mt or 1 
            wt_per_pc = quant.product_id.wt_per_pc or 1
            quant.quantity_mtr = quant.inventory_quantity_auto_apply / wt_per_mt
            quant.quantity_pcs = quant.inventory_quantity_auto_apply / wt_per_pc
