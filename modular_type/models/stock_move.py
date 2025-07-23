# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    modular_type_id = fields.Many2one(
        "modular.types",
        string="Modular Type",
        compute="_compute_modular_type",
        store=True
    )
    multiplied_product_uom_qty = fields.Float(
        'Multiplied Demand',
        compute="_compute_multiplied_product_uom_qty",
        inverse="_inverse_multiplied_product_uom_qty",
        store=True
    )

    @api.depends("product_id", "raw_material_production_id")
    def _compute_modular_type(self):
        for move in self:
            move.modular_type_id = False
            if move.product_id and move.raw_material_production_id:
                bom = move.raw_material_production_id.bom_id
                if bom:
                    bom_line = self.env["mrp.bom.line"].search([
                        ("bom_id", "=", bom.id),
                        ("product_id", "=", move.product_id.id)
                    ], limit=1)

                    if bom_line and bom_line.modular_type_id:
                        move.modular_type_id = bom_line.modular_type_id.id

    @api.depends('product_id', 'modular_type_id')
    def _compute_multiplied_product_uom_qty(self):
        for move in self:
            bom = self.env['mrp.bom.line'].search(
                [('product_tmpl_id', '=', move.product_id.product_tmpl_id.id)], limit=1)
            if move.product_id and move.modular_type_id:
                move.multiplied_product_uom_qty = move.modular_type_id.quantity_multiplier * bom.product_qty
            elif move.product_id and not move.modular_type_id:
                move.multiplied_product_uom_qty = move.product_uom_qty

    def _inverse_multiplied_product_uom_qty(self):
        for move in self:
            if move.product_id and move.modular_type_id:
                if move.modular_type_id.quantity_multiplier:
                    move.product_uom_qty = move.multiplied_product_uom_qty / \
                        move.modular_type_id.quantity_multiplier
                else:
                    move.product_uom_qty = move.multiplied_product_uom_qty
            else:
                move.product_uom_qty = move.multiplied_product_uom_qty
