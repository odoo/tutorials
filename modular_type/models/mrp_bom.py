# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    modular_type_id = fields.Many2one(
        "mrp.bom.line", related='bom_line_ids.modular_type_id')
