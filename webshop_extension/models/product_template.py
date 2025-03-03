from odoo import fields, models
from odoo.tools.translate import html_translate


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    extended_description = fields.Html(
        string="Extended Product Description",
        translate=html_translate,
    )
