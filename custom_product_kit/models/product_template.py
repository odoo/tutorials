from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean()
    sub_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Sub-Products",
        required=True,
    )

    @api.constrains("sub_product_ids")
    def _check_kit_in_subproducts(self):
        """Kit product itself must not be included in subproduct!"""
        if self in self.sub_product_ids.mapped("product_tmpl_id"):
            raise ValidationError(
                "A kit product cannot be included in its own sub-products!"
            )
