from odoo import Command, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def copy(self, default=None):
        """Override copy to ensure only product lines are copied and deposit lines are recreated."""
        default = dict(default or {})
        default.update(order_line=[Command.set([])])
        new_orders = super().copy(default)
        for old_order, new_order in zip(self, new_orders):
            filtered_lines = old_order.order_line.filtered(lambda line: not line.is_deposit_line)
            new_order.write({
                'order_line': [Command.create(line.copy_data()[0]) for line in filtered_lines]
            })
        return new_orders
