from odoo import api, models, fields
from odoo.exceptions import ValidationError

class ProductKit(models.Model):
    _inherit = "product.template"
    
    is_kit = fields.Boolean(string="Is Kit")
    kit_product_ids = fields.Many2many("product.product", "kit_product_m2m", "kit_id", "product_id")
    
    @api.constrains("kit_product_ids")
    def _check_main_product_not_in_kit_products(self):
        """ Prevent main product from being added as its own sub-product. """
        for product in self:
            if product.product_variant_id in product.kit_product_ids:
                raise ValidationError("The main product cannot be added as a sub-product in its own kit.")
