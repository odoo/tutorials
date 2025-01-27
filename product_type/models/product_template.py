from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean(default=False, string="Kit")
    kit_product_ids = fields.One2many(
        "product.product", "kit_product_template_id", string="product_ids"
    )
