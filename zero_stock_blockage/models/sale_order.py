from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_approval = fields.Boolean(string="Approval")
    is_approval_read = fields.Boolean(compute="_compute_is_approval_read")

    @api.depends_context("uid")
    def _compute_is_approval_read(self):
        is_user_manager = self.env.user.has_group("sales_team.group_sale_manager")
        for record in self:
            if is_user_manager:
                record.is_approval_read = True
            else:
                record.is_approval_read = False

    def action_confirm(self):
        if not self.is_approval:
            raise UserError("You are not authenticated to Confirm Sale Order")

        return super().action_confirm()
