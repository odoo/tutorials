# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    s_quantity = fields.Float(
        string="S. Quantity",
        compute="_compute_s_quantity",
        store=True
    )
    s_unit = fields.Selection(
                selection=[("kg", "Kg"),
                   ("mtrs", "Mtrs."),
                   ("pcs", "PCs."),],
        string="S. Unit",
        compute="_compute_s_unit",
        store=True,
        recursive=True
    )

    @api.depends('procurement_group_id.sale_id.order_line.product_uom', 'procurement_group_id.mrp_production_ids.s_unit', 's_unit')
    def _compute_s_unit(self):
        for record in self:
            sale_order = record.procurement_group_id.sale_id
            source_mo = record.procurement_group_id.mrp_production_ids[:1]
            if sale_order and sale_order.order_line:
                record.s_unit = sale_order.order_line[0].s_unit
            elif source_mo:
                record.s_unit = source_mo.s_unit
            else:
                record.s_unit = False

    @api.depends('product_id', 'product_qty', 's_unit')
    def _compute_s_quantity(self):
        for record in self:
            wt_per_mt = record.product_id.wt_per_mt if record.product_id.wt_per_mt else 1
            wt_per_pc = record.product_id.wt_per_pc if record.product_id.wt_per_pc else 1
            if record.s_unit == "mtrs":
                record.s_quantity = record.product_qty / wt_per_mt
            elif record.s_unit == "pcs":
                record.s_quantity = record.product_qty / wt_per_pc
            else:
                record.s_quantity = 0
