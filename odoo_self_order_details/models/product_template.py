from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    self_order_description = fields.Html(string="Self Order Description")
