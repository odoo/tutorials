from odoo import models, fields, api


class GlobalInfoLine(models.Model):
    _name = "global.info.line"
    _description = "Global Info Line"

    order_id = fields.Many2one(
        comodel_name='sale.order',
        string="Order Reference",
        required=True,
        ondelete='cascade',
        index=True,
    )
    product_category_id = fields.Many2one(
        comodel_name='product.category',
        string="Product Category",
        readonly=True,
    )
    attribute_id = fields.Many2one(
        comodel_name='product.attribute',
        string="Attribute",
        readonly=True,
    )
    attribute_value_id = fields.Many2one(
        comodel_name='product.attribute.value',
        string="Attribute Value",
        domain="[('attribute_id', '=', attribute_id)]",
    )
