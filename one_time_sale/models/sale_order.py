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
        self.ensure_one()

        product = order_line.product_id if order_line.product_id.id else self.env['product.product'].browse(product_id)

        if product.recurring_invoice:
            if not kwargs.get('plan_id'):
                if order_line and quantity <= 0:
                    # Remove zero or negative lines
                    order_line.unlink()
                    order_line = self.env['sale.order.line']
                    self.plan_id = False
                elif order_line:
                    # Update existing line
                    update_values = self._prepare_order_line_update_values(order_line, quantity, **kwargs)
                    if update_values:
                        self._update_cart_line_values(order_line, update_values)
                elif quantity > 0:
                    # Create new line
                    order_line_values = self._prepare_order_line_values(product_id, quantity, **kwargs)
                    order_line = self.env['sale.order.line'].sudo().create(order_line_values)
                return order_line
        
        return super()._cart_update_order_line(product_id, quantity, order_line, **kwargs)
