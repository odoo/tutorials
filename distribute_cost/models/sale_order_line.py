from odoo import api, models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    original_sale_order_line_id = fields.Many2one('sale.order.line', string="Original Line")
    distribution_tag_ids = fields.Many2many('sale.order.line.distribution.tag', string='Cost Distribution Tags')
    
    def action_open_distribute_cost_wizard(self):
        self.ensure_one()
        return {
            'name': 'Distribute Cost',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.distribute.cost.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'order_id': self.order_id.id,
                'product_line_id': self.id,
            }
        }
    
    def unlink(self):
        for line in self:
            if line.original_sale_order_line_id:
                # Only add back the portion of the price that was distributed
                total_price_to_return = 0
                distribute_wizard = self.env['sale.order.distribute.cost.wizard'].search([
                    ('distribution_line_ids.sale_order_line_id', '=', line.id)
                ], limit=1)

                if distribute_wizard:
                    for dist_line in distribute_wizard.distribution_line_ids:
                        if dist_line.sale_order_line_id == line:
                            total_price_to_return += dist_line.allocated_price

                # Add only the divided amount back to the original line
                line.original_sale_order_line_id.price_subtotal += total_price_to_return

        return super(SaleOrderLine, self).unlink()
