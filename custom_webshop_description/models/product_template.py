from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ecommerce_extended_description = fields.Html(
        string='Ecommerce Extended Description',
        translate=True,
        help="Extended product description with multilingual support."
    )
