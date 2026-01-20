from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    self_order_description = fields.Html(
        string="Self Order Description",
        translate=True,
    )
