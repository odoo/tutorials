from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_kit = fields.Boolean(string='Is Kit', default=False)
    sub_product_ids = fields.Many2many('product.product', 'product_template_kit_component_rel')

    @api.constrains("sub_product_ids")
    def _check_no_self_product_reference(self):
        for record in self:
            if record.product_variant_ids in record.sub_product_ids:
                raise ValidationError("A product cannot be added as a sub-product in its own kit.")
