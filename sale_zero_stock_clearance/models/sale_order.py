from odoo import  api, fields, models
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(
        string="Zero Stock Approval",
         compute='_compute_zero_stock_approval',
        help="Requires approval when stock is zero"
    )
    has_group_manager = fields.Boolean(default=lambda self: self.env.user.has_group('sales_team.group_sale_manager'), store=False)

    def action_confirm(self):
        if not self.env.user.has_group('sales_team.group_sale_manager') and not self.zero_stock_approval :
            raise UserError("You cannot confirm this order because Zero Stock Approval is required.")
        return super(SaleOrder, self).action_confirm()
    
    @api.depends('order_line.free_qty_today')
    def _compute_zero_stock_approval(self):
            self.zero_stock_approval = any(line.free_qty_today <= 0 for line in self.order_line)
