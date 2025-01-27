from odoo import fields, models


class InheritedProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean(string="Is Kit", default=False)
    sub_products_ids = fields.Many2many(comodel_name="product.product", string="Sub Products")
