from odoo import api, models, fields, Command
from odoo.exceptions import UserError

class SaleOrderDistributeCostWizard(models.TransientModel):
    _name = 'sale.order.distribute.cost.wizard'
    _description = 'Sale Order Distribute Cost Wizard'

    name = fields.Char(string="Distribution Name")
    sale_order_id = fields.Many2one("sale.order", string="Sales Order", required=True)
    distribution_line_ids = fields.One2many('sale.order.distribute.cost.line.wizard', 'wizard_id', string='Cost Distribution Lines')

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        sale_order_id = self.env.context.get("order_id")

        if not sale_order_id:
            return res

        sale_order = self.env["sale.order"].browse(sale_order_id)
        sale_order_line_id = self.env.context.get("product_line_id")
        sale_order_line = self.env["sale.order.line"].browse(sale_order_line_id)

        # Get eligible lines (excluding the one being distributed)
        eligible_lines = sale_order.order_line.filtered(lambda l: l.id != sale_order_line_id)

        if not eligible_lines:
            return res

        # Evenly divide cost
        product_price = sale_order_line.price_subtotal / len(eligible_lines)

        distributed_cost_lines = []
        for line in eligible_lines:
            distributed_cost_lines.append({
                "product_id": line.product_id.id,
                "allocated_price": product_price,
                "sale_order_line_id": line.id,
                "is_selected": True  # Default checked
            })

        res.update({
            "sale_order_id": sale_order.id,
            "distribution_line_ids": [Command.clear()] + [Command.create(vals) for vals in distributed_cost_lines],
        })

        return res

    def action_confirm(self):
        sale_order_line_id = self.env.context.get("product_line_id")
        sale_order_line = self.env["sale.order.line"].browse(sale_order_line_id)
        max_allowed_amount = sale_order_line.price_subtotal

        valid_lines = self.distribution_line_ids.filtered(lambda l: l.is_selected)

        if not valid_lines:
            raise UserError("At least one order line must be selected for cost distribution.")

        distributed_amount = sum(valid_lines.mapped("allocated_price"))

        if distributed_amount > max_allowed_amount:
            raise models.ValidationError(f"Total distributed amount cannot exceed {max_allowed_amount}.")

        for line in valid_lines:
            line.sale_order_line_id.price_unit += line.allocated_price
            self._assign_distribution_tag(line.sale_order_line_id, line.allocated_price)
            line.sale_order_line_id.original_sale_order_line_id = sale_order_line_id

        remaining_amount = max_allowed_amount - distributed_amount
        sale_order_line.price_unit = remaining_amount

    def _assign_distribution_tag(self, line, amount):
        if amount != 0.0:
            tag_model = self.env["sale.order.line.distribution.tag"]
            price_tag = tag_model.search([("name", "=", amount)], limit=1)
            if not price_tag:
                price_tag = tag_model.create({'name': round(amount, 2)})
            line.distribution_tag_ids = [(6, 0, [price_tag.id])]

    @api.onchange("distribution_line_ids")
    def _onchange_distribution_lines(self):
        selected_lines = self.distribution_line_ids.filtered(lambda l: l.is_selected)

        if selected_lines:
            sale_order_line_id = self.env.context.get("product_line_id")
            current_sale_order_line = self.env["sale.order.line"].browse(sale_order_line_id)
            total_amount = current_sale_order_line.price_subtotal

            for line in selected_lines:
                line.allocated_price = round(total_amount / len(selected_lines), 2)
