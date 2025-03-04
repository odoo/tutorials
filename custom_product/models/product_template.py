from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean("Is kit")
    kit_product_ids = fields.Many2many(
        "product.product",
        "product_template_kit_rel",  # Table name
        "template_id",  # Column linking to product.template
        "product_id",  # Column linking to product.product
        string="Sub Products",
        ondelete="cascade",
    )
