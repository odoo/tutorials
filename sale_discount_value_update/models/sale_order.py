
from odoo import models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('order_line')
    def _onchange_order_line(self):
        super()._onchange_order_line()

        discount_line_ids = self.order_line.filtered(lambda or_line: or_line.product_id == or_line.company_id.sale_discount_product_id)

        regular_lines = self.order_line.filtered(lambda or_line: or_line.product_id != or_line.company_id.sale_discount_product_id)

        if not regular_lines:
            if discount_line_ids:
                for discount_line in discount_line_ids:
                    self.order_line = [(3, discount_line.id, 0)]
            return

        total_amount_sum = sum(line.price_subtotal for line in regular_lines)

        if not discount_line_ids:
            return

        # Get the discount percentage from the configuration
        discount_config = self.env["sale.order.discount"].search([("company_id", "=", self.company_id.id)], limit=1)

        if not discount_config:
            return

        discount_percentage = discount_config.discount_percentage
        discount_amount = -(total_amount_sum * discount_percentage)

        for discount_line in discount_line_ids:
            discount_line.price_unit = discount_amount
