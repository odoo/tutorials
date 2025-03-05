from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean("Is kit")
    kit_product_ids = fields.Many2many(
        "product.product",
        "product_template_kit_rel",
        "template_id",
        "product_id",
        string="Sub Products",
        ondelete="cascade",
    )
