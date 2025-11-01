from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    check_warranty_available = fields.Boolean(
        string="Has Warranty Available",
        compute='_compute_check_warranty_available'
    )

    @api.depends('order_line.product_id')
    def _compute_check_warranty_available(self):
        for order in self:
            order.check_warranty_available = any(
                line.product_template_id.is_warranty_available for line in order.order_line
            )
