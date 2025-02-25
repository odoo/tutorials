from odoo import fields,models,api,_, Command
from odoo.exceptions import ValidationError

class DistributeCostWizard(models.TransientModel):
    _name = "distribute.cost.wizard"
    _description = "Distribute cost Wizard"

    def _default_order_line_id(self):
        current_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
        order_id = current_line.order_id
        initials_lines = order_id.order_line
        add_lines = initials_lines - current_line
        pricde_to_add = (current_line.price_subtotal)/len(add_lines)
        return [
            Command.create({'name': line.name, 'divided_price': pricde_to_add, 'linked_sale_order_line_id': line.id})
            for line in add_lines
        ]
    order_id = fields.Many2one('sale.order', string="Order", required=True)
    order_line_ids = fields.One2many('distribute.cost.line', 'wizard_id', string="Order Lines", default=_default_order_line_id)

    def action_divide_cost(self):

        total_divided_price = sum(self.order_line_ids.mapped('divided_price'))

        # Constraint 1: Ensure sum of divided prices does not exceed the original line's price
        original_total_price = self.env.context.get('original_total_price')
        if total_divided_price > original_total_price:
            raise ValidationError("The total of divided prices cannot exceed the original line's price.")
        
        # Apply divided prices to visible lines
        total_amt = 0.0
        for line in self.order_line_ids:
            total_amt += line.divided_price
            line.linked_sale_order_line_id.divided_price = line.divided_price
        
        current_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
        current_line.divided_price = max(current_line.price_subtotal - total_amt,0.0)

        # Constraint 2: Remaining price adjustment
        remaining_price = original_total_price - total_divided_price        
        if remaining_price > 0:
            current_line.divided_price = remaining_price
        
        return {'type': 'ir.actions.act_window_close'}


class DistributeCostLine(models.TransientModel):
    _name = 'distribute.cost.line'
    _description = 'Distribute Cost Line'

    wizard_id = fields.Many2one('distribute.cost.wizard', string="Wizard")
    name = fields.Char(string="Product", required=True,default="pdt")
    divided_price = fields.Float(string="Price", default=0.0)
    linked_sale_order_line_id = fields.Many2one('sale.order.line')