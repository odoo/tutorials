from odoo import Command, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_copiable_order_lines_without_deposit(self):
        """Returns the order lines that can be copied to a new order without copying deposit order line."""
        deposit_product_id = self.env['ir.config_parameter'].get_param('rental_deposit.deposit_product_id')
        return self.order_line.filtered(lambda line: line.product_id.id != int(deposit_product_id))

    def copy_data(self, default=None):
        """Override copy_data to prevent deposit lines from being duplicated."""
        default = dict(default or {})
        default.setdefault('order_line', [])
        vals_list = super().copy_data(default=default)
        for order, vals in zip(self, vals_list):
            vals['order_line'] = [
                Command.create(line)
                for line in order._get_copiable_order_lines_without_deposit().copy_data()
            ]
        return vals_list
