from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def check_and_unpublish(self):
        enabled = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("unpublish_product.auto_unpublish_out_of_stock")
        )

        if not enabled:
            return

        for template in self:
            if all(variant.free_qty <= 0 for variant in template.product_variant_ids):
                template.website_published = False
