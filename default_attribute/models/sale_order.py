# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    global_info_attributes = fields.One2many('global.info.attribute', 'sale_order_id', string="Global Info Attributes")

    @api.model_create_multi
    def create(self, vals_list):
        """Ensure global categories & attributes are added to new sales orders."""
        orders = super().create(vals_list)
        for order in orders:
            order._populate_global_info_attributes()
        return orders

    def _populate_global_info_attributes(self, category=None, attribute_ids=None):
        """Add attributes to the sale order.
        - If `category` is provided, it processes only that category.
        - If `attribute_ids` is provided, only those attributes are added.
        - If no `category` is given, it processes all global categories.
        """
        categories = [category] if category else self.env['product.category'].search([('global_info', '=', True)])
        existing_attrs = {(attr.category_id.id, attr.attribute_id.id) for attr in self.global_info_attributes}
        attributes_data = []

        for cat in categories:
            attributes = cat.attribute_ids if attribute_ids is None else self.env['product.attribute'].browse(attribute_ids)

            for attribute in attributes:
                if (cat.id, attribute.id) not in existing_attrs:
                    default_values = self.env['product.attribute.value'].search([('attribute_id', '=', attribute.id)])
                    default_value_id = default_values[:1].id if default_values else False

                    attributes_data.append((0, 0, {
                        'category_id': cat.id,
                        'attribute_id': attribute.id,
                        'default_value_id': default_value_id,
                    }))

        if attributes_data:
            self.write({'global_info_attributes': attributes_data})

    def _remove_category_attributes(self, category, attribute_ids=None):
        """Remove all attributes linked to a category from the sale order."""
        attributes_to_remove = self.global_info_attributes.filtered(lambda attr: attr.category_id.id == category.id and (not attribute_ids or attr.attribute_id.id in attribute_ids))
        attributes_to_remove.unlink()
