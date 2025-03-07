# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _set_attributes_from_category(self):
        """Helper method to update product attributes based on category."""
        if self.categ_id:
            self.attribute_line_ids = [(5, 0, 0)]  # Clear existing attributes
            attribute_lines = []
            for attribute in self.categ_id.attribute_ids:
                attribute_lines.append((0, 0, {
                    'attribute_id': attribute.id,
                    'value_ids': [(6, 0, attribute.value_ids.ids)]
                }))
            self.attribute_line_ids = attribute_lines

    @api.onchange('categ_id')
    def _onchange_category_update_attributes(self):
        """Trigger attribute update when category changes."""
        self._set_attributes_from_category()

    def _update_attributes_from_category(self):
        """Manually update attributes from category (e.g., for batch updates)."""
        self._set_attributes_from_category()
