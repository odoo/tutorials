from odoo import Command, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_category_id = fields.Many2one(
        comodel_name='product.category',
        string="Product Category",
        compute="_compute_product_category",
        store=True
    )

    attribute_ids = fields.Many2many(
        comodel_name='product.attribute',
        string="Attributes"
    )

    attribute_value_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        string="Attribute Value"
    )

    @api.depends('product_id')
    def _compute_product_category(self):
        for line in self:
            if line.product_id and line.product_id.categ_id.show_on_global_info:
                line.product_category_id = line.product_id.categ_id
            else:
                line.product_category_id = False

    @api.onchange('product_category_id')
    def _onchange_product_category(self):
        if self.product_category_id:
            required_attributes = self.product_category_id.required_attribute_ids
            default_attribute_values = []
            default_attributes = []

            for attribute in required_attributes:
                selected_value = self.product_template_attribute_value_ids.filtered(lambda v: v.attribute_id == attribute)
                default_attributes.append(attribute.id)
                default_attribute_values.append(selected_value.product_attribute_value_id.id)
            self.attribute_ids = Command.set([default_attributes])
            self.attribute_value_ids = Command.set([default_attribute_values])
