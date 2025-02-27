from odoo import api, exceptions, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(string="Zero Stock Approval")
    is_sales_manager = fields.Boolean(compute='_is_sales_manager')

    def _is_sales_manager(self):
        for sale_order in self:
            sale_order.is_sales_manager = sale_order.env.user.has_group('sales_team.group_sale_manager')
        
    def action_confirm(self):
        if not self.zero_stock_approval:
            raise exceptions.ValidationError("You can not confirm this sales order because zero stock blocklist is not enable")
        return super().action_confirm()
