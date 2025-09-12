
from odoo import models, fields
from odoo.exceptions import UserError


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(
        string="Approval",
        default=False,
        readonly=False,
        help="If checked then sales user can confirm the sale order",
    )
    is_manager = fields.Boolean(default=False, compute="_compute_access_approval")

    def action_confirm(self):
        self.ensure_one()
        if (not self.zero_stock_approval and self.is_manager):
            raise UserError("You are not allowed to confirm this order as Zero Stock Approval is required.")
        return super().action_confirm()

    def _compute_access_approval(self):
        self.ensure_one()
        if self.env.user.has_group("sales_team.group_sale_manager"):
            self.is_manager = False
        else:
            self.is_manager = True
