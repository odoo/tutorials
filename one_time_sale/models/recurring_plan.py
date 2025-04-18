from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    @api.depends('order_line', 'order_line.product_id', 'order_line.product_id.recurring_invoice', 'order_line.product_id.accept_one_time')
    def _compute_has_recurring_line(self):
        for order in self:
            has_recurring = any(
                line.product_id.recurring_invoice and not line.product_id.product_tmpl_id.accept_one_time
                for line in order.order_line
            )
            order.has_recurring_line = has_recurring
