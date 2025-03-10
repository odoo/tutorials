# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    attribute_ids = fields.Many2many("product.attribute", "product_category_attribute_rel", "category_id", "attribute_id", string="Attributes")
    global_info = fields.Boolean(string="Global Info")

    def write(self, vals):
        old_global_info = {cat.id: cat.global_info for cat in self}
        old_attributes = {cat.id: set(cat.attribute_ids.ids) for cat in self}
        res = super().write(vals)

        # If category attributes are changed, update related products
        if 'attribute_ids' in vals:
            for category in self:
                products = self.env['product.template'].search([('categ_id', '=', category.id)])
                for product in products:
                    product._update_attributes_from_category()

        sales_orders = self.env['sale.order'].search([])
        for category in self:
            was_global = old_global_info.get(category.id, False)
            is_now_global = category.global_info

            old_attr_ids = old_attributes.get(category.id, set())
            new_attr_ids = set(category.attribute_ids.ids)

            if is_now_global and not was_global:
                # If category was just marked global, add it to all sales orders
                for order in sales_orders:
                    order._populate_global_info_attributes(category)

            elif not is_now_global and was_global:
                # If category was just removed from global, delete it from all sales orders
                for order in sales_orders:
                    order._remove_category_attributes(category)

            if is_now_global:
                # Handle attribute changes
                added_attrs = new_attr_ids - old_attr_ids
                removed_attrs = old_attr_ids - new_attr_ids

                for order in sales_orders:
                    if added_attrs:
                        order._populate_global_info_attributes(category, added_attrs)
                    if removed_attrs:
                        order._remove_category_attributes(category, removed_attrs)
        return res
