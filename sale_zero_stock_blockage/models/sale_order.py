from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    zero_stock_approval = fields.Boolean(string="Zero Stock Approval")
    has_user_access = fields.Boolean(compute="_compute_has_user_access")

    @api.depends_context("uid")
    def _compute_has_user_access(self):
        has_access = self.env.user._is_admin()
        for record in self:
            record.has_user_access = not has_access

    def action_confirm(self):
        for order in self:
            if not order.zero_stock_approval:
                raise UserError("Please confirm the zero stock approval")

        return super().action_confirm()
