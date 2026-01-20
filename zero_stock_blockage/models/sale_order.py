# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import  fields, models, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(string="Zero Stock Approval")
    zero_stock_readonly = fields.Boolean(compute="_compute_zero_stock_readonly")

    @api.depends("zero_stock_approval")
    def _compute_zero_stock_readonly(self):
        for record in self:
            record.zero_stock_readonly = (
                self.env.user.has_group("sales_team.group_sale_salesman") and
                not self.env.user.has_group("sales_team.group_sale_manager")
            )

    def action_confirm(self):
        for order in self:
            if not order.zero_stock_approval:
                raise UserError("You need Zero Stock Approval to confirm this sale order.")
        return super().action_confirm()
