from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    zero_stock_approval = fields.Boolean(string="Zero Stock Approval")
    approval = fields.Boolean(compute="_compute_approval")

    def _action_confirm(self):
        for order in self:
            if not order.zero_stock_approval:
                for line in order.order_line:
                    if line.product_uom_qty > line.product_id.qty_available:
                        raise UserError(
                            "Ordered quantity exceeds available stock Approval From Administration Required Before Confirming Order"
                        )
        return super(SaleOrder, self)._action_confirm()

    @api.depends_context("uid")
    def _compute_approval(self):
        self.approval = self.env.user.has_group("sales_team.group_sale_manager")
