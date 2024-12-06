from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    warranty = fields.Boolean(string="Is Warranty Available ?", default=False)
