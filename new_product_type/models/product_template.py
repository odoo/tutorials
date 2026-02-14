from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean()
    sub_product = fields.Many2many("product.product")

    @api.constrains("sub_product")
    def _check_no_self_product_reference(self):
        for record in self:
            if record.product_variant_id in record.sub_product:
                raise ValidationError("A product cannot be added as a sub-product in its own kit.")
