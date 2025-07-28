from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        for order in orders:
            order._add_deposit_lines()
        return orders

    def _add_deposit_lines(self):
        for line in self.order_line:
            product = line.product_id
            if product.require_deposit:
                exists = self.order_line.filtered(
                    lambda l: l.is_deposit_line and l.product_id == product
                )
                if not exists:
                    self.env['sale.order.line'].create({
                        'order_id': self.id,
                        'product_id': product.id,
                        'name': f"Deposit for {product.display_name}",
                        'product_uom_qty': line.product_uom_qty,
                        'price_unit': product.deposit_amount,
                        'is_deposit_line': True,
                    })

    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        res = super()._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, **kwargs)
        self._add_deposit_lines()

        return res
