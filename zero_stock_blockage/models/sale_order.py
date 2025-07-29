from odoo import api, models, fields
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    stock_approval = fields.Boolean(string='Zero Stock Approvalexchttps')
    stock_approval_readonly = fields.Boolean(compute='_compute_stock_approval_readonly')

    @api.depends_context('uid')
    def _compute_stock_approval_readonly(self):
        self.stock_approval_readonly = self.env.user.has_group('sales_team.group_sale_manager')

    def action_confirm(self):
        for records in self:
            if not records.stock_approval:
                raise UserError("You are not allowed to confirm this order unless 'Zero Stock Approvalexchttps' is enabled.")
        return super().action_confirm()
