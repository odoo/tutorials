from odoo import api, fields, models
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(string="Zero Stock Approval", default=False, help="Allow sale users to confirm the SO & avoid stock blockage.")
    is_manager = fields.Boolean(compute="_compute_is_manager")

    def _compute_is_manager(self):
        for record in self:
            record.is_manager = self.env.user.has_group('sales_team.group_sale_manager')

    #override the action_confirm method in sale.order model
    def action_confirm(self):
        for order in self:
            if not order.zero_stock_approval and not order.is_manager:
                raise UserError("Cannot confirm Sale Order without Admin permission")
            if not order.zero_stock_approval and any(line.product_id.qty_available <= 0 for line in order.order_line):
                raise UserError("Cannot confirm Sale Order because one or more products have 0 available quantity.")
        return super().action_confirm()
