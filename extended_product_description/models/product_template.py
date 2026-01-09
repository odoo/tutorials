from odoo import fields, models
from odoo.tools.translate import html_translate


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    extended_product_description = fields.Html(string='Extended product description',
        translate=html_translate,
        sanitize_overridable=True,
        sanitize_attributes=False,
        )
