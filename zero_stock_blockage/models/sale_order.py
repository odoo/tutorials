from odoo import api, fields, models, exceptions


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(string='Approval')
    zero_stock_approval_readonly = fields.Boolean(compute='_compute_readonly', store=False)

    @api.depends('zero_stock_approval')
    def _compute_readonly(self):
        """Make `zero_stock_approval` readonly for Sales Users"""
        for order in self:
            order.zero_stock_approval_readonly = not order.env.user.has_group('sales_team.group_sale_manager')

    def action_confirm(self):
        """Prevent confirmation if `zero_stock_approval` is False"""
        for order in self:
            if not order.zero_stock_approval:
                raise exceptions.ValidationError("You cannot confirm this sales order because Zero Stock Approval is not enabled.")
        return super().action_confirm()
