from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean(string="Is Kit")
    sub_product_ids = fields.Many2many("product.product", string="Sub Products")

    @api.constrains("sub_product_ids")
    def check_sub_product_not_itself(self):
        for record in self:
            if record.id in record.sub_product_ids.mapped("product_tmpl_id.id"):
                raise ValidationError(
                    "A product cannot be added as its own sub-product"
                )

    @api.constrains("sub_product_ids", "is_kit")
    def check_sub_product(self):
        for record in self:
            if record.is_kit and not record.sub_product_ids:
                raise ValidationError(
                    "A kit product must have at least one sub-product"
                )
