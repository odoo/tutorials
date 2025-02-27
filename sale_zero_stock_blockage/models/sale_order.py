from odoo import fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    zero_stock_approval = fields.Boolean(string="Zero Stock Approval")
    is_sales_manager = fields.Boolean(compute="_compute_is_sales_manager")

    def action_confirm(self):
        for order in self:
            for line in order.order_line:
                if (line.product_uom_qty > line.product_id.qty_available) and (
                    not order.zero_stock_approval
                ):
                    raise UserError(
                        "Can't confirm the order with zero stock without approval."
                    )
        return super().action_confirm()

    def _compute_is_sales_manager(self):
        for order in self:
            order.is_sales_manager = order.env.user.has_group('sales_team.group_sale_manager')
