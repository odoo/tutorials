from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    zero_stock_approval = fields.Boolean(string="Approval")
    approval = fields.Boolean(compute="_compute_approval", string="approval")

    def action_confirm(self):
        if not self.zero_stock_approval:
            raise UserError("You cannot create sales order without approval")
        return super().action_confirm()

    @api.depends_context("uid")
    def _compute_approval(self):
        self.approval = self.env.user.has_group("sales_team.group_sale_manager")
