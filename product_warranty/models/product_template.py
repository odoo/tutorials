from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_warrenty_available = fields.Boolean("Is Warrenty Available")
