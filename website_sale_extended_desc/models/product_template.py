# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    extended_description_ecommerce = fields.Html(
        string="Extended eCommerce Description",
        translate=True,
        sanitize_attributes=True,
        sanitize_form=True,
        exportable=True,
        readonly=False,
    )
