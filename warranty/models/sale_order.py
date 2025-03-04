from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    has_warranty_product = fields.Boolean(compute="_compute_has_warranty_product", default=False)

    @api.depends("order_line")
    def _compute_has_warranty_product(self):
        for order in self:
            order.has_warranty_product = any(
                line.product_id.is_warranty_available for line in order.order_line if line.product_id
            )
