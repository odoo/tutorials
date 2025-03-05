# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    show_warranty_button = fields.Boolean(string="Show Warranty Button", compute='_compute_show_warranty_button')

    def open_warranty_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add Warranty',
            'res_model': 'add.warranty.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_sale_order_id': self.id}
        }

    @api.depends("order_line.product_id")
    def _compute_show_warranty_button(self):
        self.show_warranty_button = any(line.product_template_id.warranty_available for line in self.order_line)
