from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    has_warranty = fields.Boolean(default=False)