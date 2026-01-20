from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean(string="Is Kit?")
    sub_products = fields.Many2many("product.product", string="Sub Products")
