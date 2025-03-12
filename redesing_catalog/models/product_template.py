from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    package_field = fields.Char(string="Package Details")


class ProductProduct(models.Model):
    _inherit = "product.product"

    package_field = fields.Char(related="product_tmpl_id.package_field", store=True)
