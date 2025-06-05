from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean("Is kit")
    sub_product_ids = fields.Many2many(
        "product.product", string="sub products", required=True,  domain=[('is_kit', '=', False)]
    )
