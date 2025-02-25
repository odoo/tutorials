from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_warranty = fields.Boolean(string="Is Warranty Available")
