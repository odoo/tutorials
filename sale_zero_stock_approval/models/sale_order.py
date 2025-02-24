from odoo import api, fields, models
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(string="Zero Stock Approval", help="If True, the sales manager can confirm the sale order even if stock is unavailable.")

    #override the action_confirm method in sale.order model
    def action_confirm(self):
        for order in self:
            if not order.zero_stock_approval:
                for line in order.order_line:
                    available_qty = line.product_id.qty_available
                    if available_qty <= 0 :
                        raise UserError("Cannot confirm Sale Order because the product has 0 available quantity")
        return super().action_confirm()
