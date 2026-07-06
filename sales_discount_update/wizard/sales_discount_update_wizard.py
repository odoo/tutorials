from odoo import models


class SaleOrderDiscount(models.TransientModel):
    _inherit = 'sale.order.discount'

    def action_apply_discount(self):
        self.ensure_one()

        if self.discount_type == 'so_discount':
            order = self.sale_order_id

            discount_lines = order.order_line.filtered(
                lambda line: line._is_global_discount()
            )

            if discount_lines:
                discount_lines.with_context(
                    skip_global_discount_update=True
                ).unlink()

            order.global_discount_percentage = (
                self.discount_percentage * 100
            )

        return super().action_apply_discount()
