from odoo import fields, models
from odoo.tools.translate import html_translate
from odoo.tools import html2plaintext


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ecom_extended_description = fields.Html(
        string='Ecommerce extended description',
        translate=html_translate,
        help='add detailed desription of the product use "/" for formating'
    )

    def get_clean_description(self):
        return html2plaintext(self.ecom_extended_description or '').strip()
