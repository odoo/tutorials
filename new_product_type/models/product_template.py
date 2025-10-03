from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean(string="Is Kit", default=False)
    sub_products = fields.Many2many(
        "product.product",
        string="Sub Products",
        help="Select the products that are part of this kit",
        domain="[('is_kit', '=', False)]",
    )
