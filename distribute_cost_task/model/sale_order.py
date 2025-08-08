from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    divide_column = fields.Boolean(
        string="Divide Column",
        compute="_compute_divide_column",
        store=True,
        default=False,
    )

    @api.depends("order_line.divide_cost")
    def _compute_divide_column(self):
        data = dict(
            self.env["order.line.cost.divide"]._read_group(
                [("order_id", "in", self.ids)], ["order_id"], ["__count"]
            )
        )
        for order in self:
            if data.get(order):
                has_zero_divide_cost = any(
                    line.divide_cost == 0 for line in order.order_line
                )
                order.divide_column = has_zero_divide_cost

    def _get_order_lines_to_report(self):
        order_lines = super()._get_order_lines_to_report()
        return order_lines.filtered(
            lambda line: not line.divide_from_order_lines or line.divide_cost > 0
        )
