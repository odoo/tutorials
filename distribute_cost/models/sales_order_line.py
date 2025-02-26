from email.policy import default
from odoo import fields, models,api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    divided_price = fields.Float(string="Division", default="0.0")
    parent_division_id = fields.Many2one('sale.order.line')
    def action_distribute_cost(self):
        order = self.order_id
        total_price = self.price_subtotal
        return {
            'type': 'ir.actions.act_window',
            'name': 'Distribute Cost',
            'res_model': 'distribute.cost.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_id': order.id,        
                'original_total_price': total_price,
            },
        }
    
    def unlink(self):
        print 
        for line in self:
            if(not line.parent_division_id.id):
                child_lines = self.env['sale.order.line'].search([('parent_division_id', '=', line.id)])
                for child in child_lines:
                    child.price_subtotal = child.price_subtotal - child.divided_price
                    child.divided_price = 0.0
            elif(line.parent_division_id.id):
                child_lines = self.env['sale.order.line'].search([('parent_division_id', '=', line.id)])
                for child in child_lines:
                    child.divided_price -= (line.price_unit * line.product_uom_qty)/len(child_lines)
                    child.price_subtotal = child.divided_price + (child.price_unit * child.product_uom_qty)
            else:
                line.parent_division_id.divided_price += line.divided_price
        return super().unlink()
    