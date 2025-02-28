# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'
            
    @api.onchange('order_line')
    def _onchange_order_line(self):
        """Add or update deposit lines when rental products are added/changed"""
        deposit_product_id = int(self.env['ir.config_parameter'].sudo().get_param(
            'sale_renting.deposit_product_id', False))
        
        if not deposit_product_id:
            return
            
        for line in self.order_line.filtered(lambda l: not l.is_deposit_line):
            if line.product_id.require_deposit:
                existing_deposit = self.order_line.filtered(
                    lambda l: l.is_deposit_line and 
                             l.linked_product_id.id == line.product_id.id)
                
                deposit_amount = line.product_id.deposit_amount * line.product_uom_qty
                
                if not existing_deposit:
                    self.order_line = [(0, 0, {
                        'product_id': deposit_product_id,
                        'name': f'Deposit for {line.product_id.name}',
                        'product_uom_qty': 1,
                        'price_unit': deposit_amount,
                        'is_deposit_line': True,
                        'linked_product_id': line.product_id.id,
                    })]
                else:
                    existing_deposit.price_unit = deposit_amount
