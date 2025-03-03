from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProducTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean(string="Is kit")
    sub_product_ids = fields.Many2many(
        "product.product", string="Sub Product", required=True
    )

    @api.constrains("sub_product_ids")
    def _check_no_self_reference(self):
        for record in self:
            if record.product_variant_id in record.sub_product_ids:
                raise ValidationError("A product cannot be part of its own sub-products list")
