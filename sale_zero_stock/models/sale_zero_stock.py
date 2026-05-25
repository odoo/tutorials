from odoo import fields, models, api
from odoo.exceptions import UserError


class SaleZeroStock(models.Model):
    _inherit = "sale.order"

    zero_stock_approval = fields.Boolean(string="Zero Stock Approval")
    access_user = fields.Boolean(compute="_compute_has_access")

    @api.depends_context("uid")
    def _compute_has_access(self):

        has_user_access = self.env.user._is_admin()
        for record in self:
            record.access_user = not has_user_access

    def action_confirm(self):
        for order in self:
            if not order.zero_stock_approval:
                raise UserError("Please confirm the zero stock approval")

        return super().action_confirm()
