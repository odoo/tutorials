# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo.http import request, route
from odoo.addons.sale.controllers.product_configurator import SaleProductConfiguratorController


class DefaultAttributeController(SaleProductConfiguratorController):

    @route(route='/sale/product_configurator/get_values', type='json', auth='user')
    def sale_product_configurator_get_values(
        self,
        product_template_id,
        quantity,
        currency_id,
        so_date,
        product_uom_id=None,
        company_id=None,
        pricelist_id=None,
        ptav_ids=None,
        only_main_product=False,
        **kwargs,
    ):
        """Ensure ptav_ids use the latest default_value_id from global.info.attribute"""
        product_template = request.env['product.template'].browse(product_template_id)
        product_category = product_template.categ_id
        global_attributes = request.env['global.info.attribute'].search([
            ('category_id', '=', product_category.id),
            ('default_value_id', '!=', False)
        ])

        if not global_attributes:
            _logger.warning(f"⚠️ No global attributes found for category {product_category.name}. Default values will not be applied!")

        ptav_ids = []
        processed_attributes = set()  # Keep track of attributes to avoid duplicates

        for attr in global_attributes:
            if attr.attribute_id.id in processed_attributes:
                continue  # Skip if we've already processed this attribute

            ptav = request.env['product.template.attribute.value'].search([
                ('attribute_id', '=', attr.attribute_id.id),
                ('product_tmpl_id', '=', product_template.id),
                ('product_attribute_value_id', '=', attr.default_value_id.id),
            ], limit=1)

            if ptav:
                ptav_ids.append(ptav.id)
                processed_attributes.add(attr.attribute_id.id)  # Mark attribute as processed
            else:
                _logger.warning(f"⚠️ No PTAV found for Attribute {attr.attribute_id.name} → Value {attr.default_value_id.id}")

        # # Call the original method with updated ptav_ids
        response = super().sale_product_configurator_get_values(
            product_template_id,
            quantity,
            currency_id,
            so_date,
            product_uom_id,
            company_id,
            pricelist_id,
            ptav_ids=ptav_ids,
            only_main_product=only_main_product,
            **kwargs,
        )
        response['force_update'] = True
        return response
