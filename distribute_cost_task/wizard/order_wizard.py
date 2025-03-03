from odoo import api, fields, models
from odoo.exceptions import UserError


class OrderLineWizard(models.TransientModel):
    _name = 'order.wizard'
    _description = 'Order Line Wizard'

    order_line_ids = fields.One2many('order.line.wizard', 'wizard_id', string="Order Lines")
    exclude_line_id = fields.Many2one('sale.order.line', string="Order Line")

    @api.model
    def default_get(self, fields_list):
        res = super(OrderLineWizard, self).default_get(fields_list)
        exclude_line_id = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
        exclude_line_cost = exclude_line_id.price_unit
        order_lines = []
        order = self.env['sale.order'].browse(self.env.context.get('order_id'))
        total_lines = order.order_line - exclude_line_id
        if len(total_lines) == 0 :
            raise UserError("No order line to divide cost")
        cost = exclude_line_cost / len(total_lines)
        for line in order.order_line - exclude_line_id:
            order_lines.append((0, 0, {
                'product_template_id': line.product_template_id.id,
                'price': cost,
                'order_line_id': line.id,
                'include_for_division': True
            }))
        res['exclude_line_id'] = exclude_line_id.id  
        res['order_line_ids'] = order_lines
        return res

    def action_add_cost(self):
        include_for_division_lines = self.order_line_ids.filtered(lambda l: l.include_for_division)
        if not include_for_division_lines:
            raise UserError("At least one order line must be selected for cost division.")
        total_cost = 0
        line_cost = self.exclude_line_id.price_unit
        for wiz_line in include_for_division_lines:
            total_cost += wiz_line.price
        if(total_cost < line_cost):
            self.exclude_line_id.divide_cost += line_cost-total_cost
            for wiz_line in include_for_division_lines:
                wiz_line.order_line_id.divide_cost += wiz_line.price
                self.env["order.line.cost.divide"].create({
                "cost": wiz_line.price,
                "divide_from_order_line": self.exclude_line_id.id,
                "divide_to_order_line": wiz_line.order_line_id.id,
                "order_id": self.exclude_line_id.order_id.id  })
        elif(total_cost == line_cost):
            for wiz_line in include_for_division_lines:
                wiz_line.order_line_id.divide_cost += wiz_line.price
                self.env["order.line.cost.divide"].create({
                "cost": wiz_line.price,
                "divide_from_order_line": self.exclude_line_id.id, 
                "divide_to_order_line": wiz_line.order_line_id.id,
                "order_id": self.exclude_line_id.order_id.id })
        else:
            raise UserError(f"Total cost of all product greater than {line_cost}")             
