from odoo import Command, api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('order_line')
    def _onchange_order_line(self):
        """
        Triggered in the UI when order lines or global_discount changes.
        Applies the global discount to each order line.
        """
        super()._onchange_order_line()
        # Get the default discount productid
        discount_product_id = self.company_id.sale_discount_product_id

        # Separate Product lines and Discount lines [Old: without changed value, New: with changed value in UI]
        old_product_lines = self._origin.order_line.filtered(lambda line: line.product_id != discount_product_id)
        new_product_lines = self.order_line.filtered(lambda line: line.product_id != discount_product_id)
        old_discount_lines = (self._origin.order_line - old_product_lines)
        new_discount_lines = (self.order_line - new_product_lines)

        # Calculate Product total
        old_product_total = sum(old_product_lines.mapped('price_subtotal'))
        new_product_total = sum(new_product_lines.mapped('price_subtotal'))

        # If product lines exists, calculate new discount unit rates else remove discount lines
        if new_product_lines:
            old_discount_units = old_discount_lines.mapped('price_unit')
            for index, line in enumerate(new_discount_lines):
                discount_percentage = (abs(old_discount_units[index]) / old_product_total * 100) if old_product_total else 0.0
                line.price_unit = -((new_product_total * discount_percentage) / 100)
        else:
            commands = [Command.unlink(line_id) for line_id in new_discount_lines.mapped('id')]
            if commands:
                self.order_line = list(commands)
