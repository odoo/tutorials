from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    has_warranty = fields.Boolean("Is warranty Available", default=False)
