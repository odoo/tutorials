from odoo import models


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    def write(self, vals):
        res = super().write(vals)

        if 'value_ids' in vals or 'attribute_line_ids' in vals:
            self._update_sale_orders_global_info()

        if 'value_ids' in vals:
            self._update_product_template_attribute_values()         

        return res

    def _update_sale_orders_global_info(self):
        sale_orders = self.env['sale.order'].search([])
        sale_orders._generate_global_info_lines()   

    def _update_product_template_attribute_values(self):
        for attribute in self:
            products = self.env['product.template'].search([
                ('categ_id.default_attribute_ids', 'in', attribute.id)
            ])
            for product in products:
                attr_line = product.attribute_line_ids.filtered(lambda line: line.attribute_id == attribute)
                new_values = self.env['product.attribute.value'].search([('attribute_id', '=', attribute.id)])
                if attr_line:
                    attr_line.write({'value_ids': [(6, 0, new_values.ids)]})
                else:
                    product.attribute_line_ids = [(0, 0, {
                        'attribute_id': attribute.id,
                        'value_ids': [(6, 0, new_values.ids)]
                    })]
