from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.product"

    kit_product_template_id = fields.Many2one(
        "product.template",
    )  # ondelete="cascade"
