from odoo import api, models

import logging


_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = ['product.template']

    @api.model_create_multi
    def create(self, vals):
        product = super().create(vals)
        product._assign_default_attributes()
        return product

    def write(self, vals):
        res = super().write(vals)
        if 'categ_id' in vals:
            self._assign_default_attributes()
        return res

    def _assign_default_attributes(self):
        for product in self:
            if not product.categ_id:
                continue

            default_attributes = product.categ_id.default_attribute_ids
            product.attribute_line_ids = [(5,)]  
            attribute_lines = []
            for attr in default_attributes:
                attr_values = self.env['product.attribute.value'].search([('attribute_id', '=', attr.id)])
                if attr_values:
                    attribute_lines.append((0, 0, {
                        'attribute_id': attr.id,
                        'value_ids': [(6, 0, attr_values.ids)],
                    }))
                else:
                    _logger.warning(f"Attribute '{attr.name}' does not have any values, so it can't be assigned to product '{product.name}' (ID: {product.id})")
                    continue
            product.attribute_line_ids = attribute_lines
