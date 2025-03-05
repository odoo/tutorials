from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_warranty_available = fields.Boolean(string="Is Warranty Available")
