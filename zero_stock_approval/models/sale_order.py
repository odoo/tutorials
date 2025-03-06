# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    zero_stock_approval = fields.Boolean(
        string='Zero Stock Approval',
        help='If checked, sales user can confirm the sale order even with zero stock'
    )
    
    zero_stock_readonly = fields.Boolean(
        string='Zero Stock Readonly',
        description="Readonly field for sales user",
        compute='_compute_zero_stock_readonly'
    )
    
    @api.depends('zero_stock_approval')
    def _compute_zero_stock_readonly(self):
        """Compute if the field should be readonly based on user permissions"""
        for record in self:
            record.zero_stock_readonly = (
                self.env.user.has_group('sales_team.group_sale_salesman') and 
                not self.env.user.has_group('sales_team.group_sale_manager')
            )
    
    def action_confirm(self):
        """Check if zero stock approval is needed to confirm"""  
        for order in self:
            for line in order.order_line:
                product = line.product_id
                
                if product.type == 'product' or product.type == 'consu' and product.qty_available < line.product_uom_qty:
                    print("Not enough stock for", product.name)
                    if not order.zero_stock_approval:
                        raise UserError("Not enough stock! Enable Zero Stock Approval to confirm anyway.")
                    break
                
        return super(SaleOrder, self).action_confirm()
