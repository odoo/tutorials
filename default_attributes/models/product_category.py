from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = "product.category"

    attribute_ids = fields.Many2many(
        "product.attribute", "category_attribute_m2m", string="Category Attributes"
    )

    show_global_info = fields.Boolean(string="Show on Global Info tab of SO")
