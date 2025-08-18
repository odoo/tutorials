from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    category_description = fields.Char(string="Category Description")
