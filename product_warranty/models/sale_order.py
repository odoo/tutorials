from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    has_warranty = fields.Boolean(default=False, compute="_compute_has_warranty", store=True)

    @api.depends("order_line")
    def _compute_has_warranty(self):
        for record in self:
            record.has_warranty = any(
                order.product_id.is_warranty and not order.product_warranty_sale_line_id
                for order in record.order_line
            )
