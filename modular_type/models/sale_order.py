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
            line.has_modular_type = bool(
                line.product_id.product_tmpl_id.modular_types) if line.product_id else False

    def action_open_modualr_type_wizard(self):
        domain = self._context.get('domain', [])
        default_values = []

        order_line = self.env["sale.order.line"].browse(self._context.get('id'))
        product_tmpl = order_line.product_id.product_tmpl_id
        if product_tmpl:
            modular_type_lines = []
            for modular_type in product_tmpl.modular_types:
                modular_type_lines.append({
                    "type_id": modular_type.id,
                    "type_name": modular_type.name,
                    "type_value": modular_type.quantity_multiplier,
                })
            default_values = modular_type_lines

        return {
            'type': 'ir.actions.act_window',
            'name': ('ProSave Product'),
            'res_model': 'modular.type.wizard',
            'views': [[False, 'form']],
            'target': 'new',
            'context': {
                'default_modular_type_ids': default_values,
                'domain': domain,
            }
        }
