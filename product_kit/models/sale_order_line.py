# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    has_kit = fields.Boolean(compute="_compute_has_kit")

    @api.depends("product_template_id")
    def _compute_has_kit(self):
        for record in self:
            record.has_kit = record.product_template_id.has_kit
