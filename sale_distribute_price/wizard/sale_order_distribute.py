from odoo import api, fields, models
from odoo.tools import float_round
from odoo.exceptions import ValidationError


class SaleOrderDistribute(models.TransientModel):
    _name = "sale.order.distribute"
    _description = "Sale Order Distribute"

    sale_order_id = fields.Many2one("sale.order", required=True)
    product_line_ids = fields.One2many("sale.order.distribute.line", "wizard_id")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        order_id = self.env.context.get('current_order_id')
        product_line_id = self.env.context.get('current_order_line_id')

        if order_id and product_line_id:
            order = self.env['sale.order'].browse(order_id)
            current_order_line = self.env['sale.order.line'].browse(product_line_id)
            product_line_amount = current_order_line.price_subtotal

            lines = order.order_line - current_order_line

            line_data = []
            if len(lines) > 0:
                remaining_amount = product_line_amount
                for index, line in enumerate(lines):
                    if index < len(lines) - 1:
                        rounded_amount = float_round(product_line_amount / len(lines), precision_rounding=0.01)
                        remaining_amount -= rounded_amount
                    else:
                        rounded_amount = remaining_amount

                    line_data.append((0, 0, {
                        'order_line_id': line.id,
                        'product_id': line.product_id.id,
                        'is_divided': True,
                        'amount': float_round(product_line_amount / len(lines), precision_rounding=0.01),
                    }))
                    line.divided_from_line_id = current_order_line.id
            res.update({'sale_order_id': order_id, 'product_line_ids': line_data})

        return res

    @api.onchange('product_line_ids')
    def _onchange_product_line_ids(self):
        selected_lines = self.product_line_ids.filtered(lambda l: l.is_divided)

        if selected_lines:
            product_line_id = self.env.context.get("current_order_line_id")
            current_order_line = self.env["sale.order.line"].browse(product_line_id)
            total_amount = current_order_line.price_subtotal

            remaining_amount = total_amount
            for index, line in enumerate(selected_lines):
                if index < len(selected_lines) - 1:
                    rounded_amount = float_round(total_amount / len(selected_lines), precision_rounding=0.01)
                    remaining_amount -= rounded_amount
                else:
                    rounded_amount = remaining_amount

                line.amount = rounded_amount

    def action_divide_price(self):
        product_line_id = self.env.context.get("current_order_line_id")
        current_order_line = self.env["sale.order.line"].browse(product_line_id)
        max_allowed_amount = current_order_line.price_subtotal

        selected_lines = self.product_line_ids.filtered(lambda l: l.is_divided)
        distributed_amount = sum(selected_lines.mapped("amount"))

        if len(selected_lines) == 0:
            raise ValidationError("At least one line must be selected.")

        if distributed_amount > max_allowed_amount:
            raise ValidationError(f"Total distributed amount cannot exceed {max_allowed_amount}.")

        for line in selected_lines:
            line.order_line_id.price_subtotal += line.amount
            line.order_line_id.price_unit = line.order_line_id.price_subtotal/line.order_line_id.product_uom_qty
            self.add_division_tag(line.order_line_id, line.amount)

        remaining_amount = remaining_amount = float_round(max_allowed_amount - distributed_amount, precision_rounding=0.01)
        current_order_line.price_unit = remaining_amount
        self.add_division_tag(current_order_line, remaining_amount)

    def add_division_tag(self, line, amount):
        if amount != 0.0:
            division_tag = self.env["sale.order.line.division.tag"]
            name = division_tag.search([("name", "=", amount)], limit=1)

            if not name:
                name = division_tag.create({"name": float_round(amount, precision_rounding=0.01)})

            line.divided_amount_ids = [(6, 0, [name.id])]
