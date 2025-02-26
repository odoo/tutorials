from odoo import api, exceptions, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(string="Zero Stock Approval")
    group_check = fields.Boolean(compute='_group_check')

    def _group_check(self):
        if self.env.user.has_group('sales_team.group_sale_manager'):
            self.group_check = True
        else:
            self.group_check = False

    def action_confirm(self):
        if not self.zero_stock_approval:
            raise exceptions.ValidationError("You can not confirm this sales order because zero stock blocklist is not allowed")
        return super().action_confirm()
