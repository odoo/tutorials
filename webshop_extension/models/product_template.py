from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    ecommerce_extended_description = fields.Html(string="Ecommerce Extended Description", translate=True)
