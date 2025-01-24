from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_warranty = fields.Boolean(default=False, string="Warranty")


