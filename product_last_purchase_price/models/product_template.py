from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    last_purchase_price = fields.Float(
        string="Last Purchase Price",
        compute="_compute_last_purchase_price",
        store=False,
        readonly=True,
    )

    @api.depends("product_variant_ids")
    def _compute_last_purchase_price(self):
        for template in self:
            product = template.product_variant_ids[:1]
            last_po_line = self.env["purchase.order.line"].search(
                [
                    ("product_id", "=", product.id),
                    ("order_id.state", "in", ["purchase", "done"]),
                ],
                order="date_order desc",
                limit=1,
            )
            template.last_purchase_price = (
                last_po_line.price_unit if last_po_line else 0.0
            )
