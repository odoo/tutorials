from odoo import Command, fields, models
from odoo.exceptions import ValidationError

class DistributeCostWizard(models.TransientModel):
    _name = "distribute.cost.wizard"
    _description = "Distribute Cost Wizard"

    def _default_order_line_id(self):
        current_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
        order_id = current_line.order_id
        initial_lines = order_id.order_line - current_line
        price_to_add = (current_line.price_subtotal) / len(initial_lines) if len(initial_lines) > 0 else 0.0
        return [
            Command.create({
                'divided_price': price_to_add,
                'linked_sale_order_line_id': line.id,
                'include_for_division': True
            })
            for line in initial_lines
        ]

    order_id = fields.Many2one('sale.order', string="Order", required=True)
    order_line_ids = fields.One2many('distribute.cost.line', 'wizard_id', string="Order Lines", default=_default_order_line_id)

    def action_divide_cost(self):
        selected_lines = self.order_line_ids.filtered(lambda line: line.include_for_division)
        total_divided_price = sum(selected_lines.mapped('divided_price'))
        original_total_price = self.env.context.get('original_total_price')
        if total_divided_price > original_total_price:
            raise ValidationError("The total of divided prices cannot exceed the original line's price.")
        current_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))

        # Apply divided prices only to selected visible lines
        total_amt = 0.0
        for line in selected_lines:
            total_amt += line.divided_price
            line.linked_sale_order_line_id.divided_price += line.divided_price
            line.linked_sale_order_line_id.price_subtotal += line.divided_price
            line.linked_sale_order_line_id.parent_division_id = current_line.id

        current_line.divided_price = max(current_line.price_subtotal - total_amt, 0.0)
        remaining_price = original_total_price - total_divided_price
        if remaining_price > 0:
            current_line.divided_price = remaining_price
            current_line.price_subtotal = current_line.price_subtotal+remaining_price
        else:
            current_line.price_subtotal =0.0
        return {'type': 'ir.actions.act_window_close'}
    
class DistributeCostLine(models.TransientModel):
    _name = 'distribute.cost.line'
    _description = 'Distribute Cost Line'

    wizard_id = fields.Many2one('distribute.cost.wizard', string="Wizard")
    linked_sale_order_line_id = fields.Many2one('sale.order.line')
    product_id = fields.Many2one(related="linked_sale_order_line_id.product_id", string="Product", required=True)
    divided_price = fields.Float(string="Price", default=0.0)
    include_for_division = fields.Boolean(string="Include for Division", default=True)
