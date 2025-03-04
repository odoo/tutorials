from odoo import api, fields, models
from odoo.tools import float_round
from odoo.models import ValidationError


class SaleOrderLineShareWizard(models.TransientModel):
    _name = "sale.order.line.share.wizard"
    _description = "Distribute Sale Order Line Price"

    sale_order_line_id = fields.Many2one(
        "sale.order.line", string="Source Line", required=True
    )
    sale_order_id = fields.Many2one(related="sale_order_line_id.order_id", store=True)
    total_amount = fields.Float(
        compute="_compute_total_amount", string="Total Amount"
    )
    left_amount = fields.Float(compute="_compute_remaining_amount", string="Left Amount")
    is_left_amount_negative = fields.Boolean(compute="_compute_is_left_amount_negative")
    line_ids = fields.One2many(
        "sale.order.line.share.wizard.line", "wizard_id", string="Lines to Share"
    )

    @api.depends("total_amount", "line_ids")
    def _compute_remaining_amount(self):
        for wizard in self:
            wizard.left_amount = wizard.total_amount - sum(
                wizard.line_ids.mapped("amount")
            )

    @api.depends("sale_order_line_id")
    def _compute_total_amount(self):
        self.total_amount = (
            self.sale_order_line_id.price_unit * self.sale_order_line_id.product_uom_qty
        )

    @api.depends("left_amount")
    def _compute_is_left_amount_negative(self):
        self.is_left_amount_negative = self.left_amount < 0

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sale_order_line = self.env["sale.order.line"].browse(
            self.env.context.get("default_sale_order_line_id")
        )

        if sale_order_line:
            order_lines = sale_order_line.order_id.order_line.filtered(
                lambda l: l.id != sale_order_line.id
            )
            count = len(order_lines)
            amount_to_divide = (
                sale_order_line.price_unit * sale_order_line.product_uom_qty
            )
            amount_per_line = float_round(amount_to_divide / count if count else 0.0, precision_digits=2)

            lines_data = [
                (
                    0,0,{
                        "sale_order_line_id": line.id,
                        "amount": amount_per_line,
                        "is_selected": True,
                    },
                )
                for line in order_lines
            ]

            remainder = amount_to_divide - (amount_per_line * count)
            lines_data[0][2]["amount"] += remainder

            res.update(
                {
                    "sale_order_line_id": sale_order_line.id,
                    "line_ids": lines_data,
                }
            )
        return res

    def action_update_prices(self):
        total_shared = sum(
            self.line_ids.filtered(lambda l: l.is_selected).mapped("amount")
        )
        remaining_amount = self.total_amount - total_shared

        if total_shared > self.total_amount:
            raise ValidationError(
                "Total shared amount cannot exceed the original amount."
            )

        for line in self.line_ids.filtered(lambda l: l.is_selected):
            line.sale_order_line_id.price_unit += (
                line.amount / line.sale_order_line_id.product_uom_qty
            )

            self.add_division_amount(line.sale_order_line_id, float_round(line.amount,precision_digits=2))

        self.sale_order_line_id.price_unit = remaining_amount
        self.add_division_amount(self.sale_order_line_id, float_round(remaining_amount,precision_digits=2))

    def add_division_amount(self, line, amount):
        if amount != 0:
            division_obj = self.env["sale.order.line.division"]
            existing_division = division_obj.search([("amount", "=", amount)], limit=1)

            if not existing_division:
                existing_division = division_obj.create({"amount": amount})

            line.division_amount_ids = [(4, existing_division.id)]
