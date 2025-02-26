# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    has_modular_type = fields.Boolean(
        string="Has Modular Type",
        compute="_compute_has_modular_type",
        store=True
    )

    @api.depends("product_id")
    def _compute_has_modular_type(self):
        for line in self:
            if line.product_id:
                line.has_modular_type = bool(
                    line.product_id.product_tmpl_id.modular_types)
