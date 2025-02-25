from odoo import fields, models,api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    divided_price = fields.Float(string="Division", default="0.0")

    def action_distribute_cost(self):
        print("========== Action Distribute Cost Called ==========")
        order = self.order_id
        order_lines = order.order_line
        total_price = self.price_subtotal
        visible_lines = order_lines - self
        divided_price = total_price / len(visible_lines) if visible_lines else 0.0
        default_order_lines = [
            {'name': line.name, 'divided_price': divided_price, 'linked_sale_order_line_id': line.id}
            for line in visible_lines
        ]
        print("Default Order Lines :",default_order_lines)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Distribute Cost',
            'res_model': 'distribute.cost.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_id': order.id,        
                # 'default_order_line_ids': default_order_lines,
                'visible_lines':visible_lines,
                'original_total_price': total_price,
            },
        }