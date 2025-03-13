# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    show_warranty_button = fields.Boolean(compute="_compute_show_warranty_button")

    def action_open_add_warranty_wizard(self):
        self.ensure_one()
        return {
            "name": "Add Warranty",
            "type": "ir.actions.act_window",
            "res_model": "sale.order.add.warranty",
            "view_mode": "form",
            "target": "new"
        }

    @api.depends("order_line.product_id")
    def _compute_show_warranty_button(self):
        self.show_warranty_button = any(
            line.product_template_id.is_warranty_available for line in self.order_line
        )
