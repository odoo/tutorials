from odoo import api, fields, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean("Is kit")
    sub_product_ids = fields.Many2many(
        comodel_name="product.product", string="sub products", required=True
    )

    @api.constrains("is_kit", "sub_product_ids")
    def validate_sub_products(self):
        for record in self:
            if record.product_variant_id in record.sub_product_ids:
                raise UserError("A product cannot be a sub-product of itself!")
