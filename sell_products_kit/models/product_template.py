from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean()
    sub_products_ids = fields.Many2many("product.product", string="Sub products")
