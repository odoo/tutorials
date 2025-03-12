from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('order_line', 'order_line.recurring_invoice')
    def _compute_has_recurring_line(self):
        """Disable validation of plan_id for one-time product purchase."""
        recurring_orders = self.filtered(lambda order: order.order_line.filtered(
            lambda line: line.product_id.recurring_invoice and not line.product_id.accept_one_time
        ))
        recurring_orders.has_recurring_line = True
        (self - recurring_orders).has_recurring_line = False

    def _cart_update_order_line(self, product_id, quantity, order_line, **kwargs):
        """Handle subscription product plan selection with one time purchase option available."""
        order_line_exist = bool(order_line)
        order_line = super()._cart_update_order_line(product_id, quantity, order_line, **kwargs)
        
        product = order_line.product_id if order_line.product_id.id else self.env['product.product'].browse(product_id)
        # remove the plan_id/default plan_id if the subscription product is added to cart without plan_id
        if product.recurring_invoice and quantity >= 0 and not kwargs.get('plan_id'):
            if not order_line_exist:
                self.plan_id = False

        return order_line
    