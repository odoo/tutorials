from odoo import api, fields, models


class CostDistributionWizard(models.TransientModel):
    _name = 'cost.distribution.wizard'

    sale_order_id = fields.Many2one('sale.order')
    sale_order_line_id = fields.Many2one('sale.order.line')
    distribution_price = fields.Float(string="Distribution price")
    target_sale_order_lines = fields.Many2many('sale.order.line', domain="[('order_id', '=', sale_order_id), ('id', '!=', sale_order_line_id)]")
    amount = fields.Float(string="Amount")

    @api.model
    def default_get(self, fields_list):
       res = super().default_get(fields_list)
       sale_order_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
       res.update({
            'sale_order_id': sale_order_line.order_id.id,
            'sale_order_line_id': sale_order_line.id,
            'distribution_price': sale_order_line.price_subtotal
        })
       return res

    def distribute_cost_wizard_action(self):
        if not self.target_sale_order_lines:
            return
        self.amount = self.distribution_price/len(self.target_sale_order_lines)
        for line in self.target_sale_order_lines:
            line.price_subtotal += self.amount
        self.sale_order_line_id.price_subtotal = 0.0
