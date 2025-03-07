# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit="sale.order.line"

    s_quantity = fields.Float(string="S. Quantity")
    s_unit = fields.Selection(
        string="S. Unit",
        selection=[("kg", "Kg"),
                   ("mtrs", "Mtrs."),
                   ("pcs", "PCs."),],
        default="mtrs",
    )
    computed_price_unit = fields.Float(string="Computed Price", store=False)

    @api.onchange("s_quantity", "s_unit", "product_id")
    def _onchange_s_unit(self):

        if not self.product_id or not self.s_unit:
            return
        
        wt_per_mt = self.product_id.wt_per_mt or 0.0
        wt_per_pc = self.product_id.wt_per_pc or 0.0
        base_price = self.product_id.lst_price

        unit_multipliers = {
            "mtrs": wt_per_mt,
            "pcs": wt_per_pc,
            "kg": 1  
        }

        multiplier = unit_multipliers.get(self.s_unit, 1)

        self.product_uom_qty = self.s_quantity * multiplier
        self.computed_price_unit = base_price * multiplier
        self.price_unit = self.computed_price_unit
        
            
