# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    modular_type_id = fields.Many2one(
        'modular.types',
        string="Modular Type",
        domain="[('id', 'in', available_modular_type_ids)]",
        help="The modular type for this BOM line",
    )
    available_modular_type_ids = fields.Many2many(
        'modular.types', compute='_compute_available_modular_types',
        string="Available Modular Types"
    )

    @api.depends('product_id')
    def _compute_available_modular_types(self):
        for line in self:
            if line.product_id:
                line.available_modular_type_ids = line.parent_product_tmpl_id.modular_types
            else:
                line.available_modular_type_ids = False
