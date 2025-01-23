from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_warranty_product = fields.Boolean("Is Warranty Product")
