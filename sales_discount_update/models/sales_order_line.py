from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _update_global_discount(self):
        for order in self.mapped('order_id'):
            if not order.global_discount_percentage:
                continue
            discount_lines = order.order_line.filtered(
                lambda line: line._is_global_discount()
            )
            normal_lines = order.order_line.filtered(
                lambda line: not line._is_global_discount()
            )
            if not normal_lines:
                if discount_lines:
                    discount_lines.with_context(
                        skip_global_discount_update=True
                    ).unlink()
                continue
            main_discount = discount_lines[:1]
            extra_discounts = discount_lines[1:]
            if extra_discounts:
                extra_discounts.with_context(
                    skip_global_discount_update=True
                ).unlink()
            if not main_discount:
                continue
            subtotal = sum(normal_lines.mapped('price_subtotal'))
            discount_amount = (
                subtotal * order.global_discount_percentage / 100
            )
            main_discount.with_context(
                skip_global_discount_update=True
            ).write({
                'price_unit': -discount_amount,
                'name': (
                    f'Discount '
                    f'{order.global_discount_percentage:.2f}%'
                ),
            })

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        if self.env.context.get('skip_global_discount_update'):
            return lines
        normal_lines = lines.filtered(
            lambda line: not line._is_global_discount()
        )
        if normal_lines:
            normal_lines._update_global_discount()
        return lines

    def write(self, vals):
        if self.env.context.get('skip_global_discount_update'):
            return super().write(vals)

        orders = self.mapped('order_id')

        result = super().write(vals)

        for order in orders:
            order.order_line._update_global_discount()

        return result

    def unlink(self):
        if self.env.context.get('skip_global_discount_update'):
            return super().unlink()
        orders = self.mapped('order_id')
        result = super().unlink()
        for order in orders:
            order.order_line._update_global_discount()
        return result
