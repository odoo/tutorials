from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_variant_id = fields.Many2one(
        "product.product", "Product", compute="_compute_product_variant_id", store=True
    )
    display_name = fields.Char(related="product_variant_id.display_name")

    @api.depends("product_variant_ids")
    def _compute_product_variant_id(self):
        for p in self:
            p.product_variant_id = p.product_variant_ids[:1].id

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        variant_results = self.env["product.product"].name_search(
            name, args, operator, limit=limit
        )
        if not variant_results:
            return []
        variant_ids = [res[0] for res in variant_results]
        variants = self.env["product.product"].browse(variant_ids)
        templates = variants.mapped("product_tmpl_id")
        return [(t.id, t.display_name) for t in templates][:limit]
