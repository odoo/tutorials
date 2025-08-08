# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class GlobalInfoAttribute(models.Model):
    _name = 'global.info.attribute'
    _description = "Global Info Attribute"

    sale_order_id = fields.Many2one('sale.order', string="Sale Order")
    category_id = fields.Many2one('product.category', string="Category")
    attribute_id = fields.Many2one('product.attribute', string="Attribute")
    default_value_id = fields.Many2one('product.attribute.value', string="Default Value", domain="[('attribute_id', '=', attribute_id)]")

    @api.onchange('default_value_id')
    def _onchange_default_value_id(self):
        """Display the new value of default_value_id when changed."""
        for record in self:
            if record.default_value_id:
                return {
                    'warning': {
                        'title': "Attribute Value Changed",
                        'message': f"New value for {record.attribute_id.name}: {record.default_value_id.name}"
                    }
                }
