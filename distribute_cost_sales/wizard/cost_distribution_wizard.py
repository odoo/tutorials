from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_round


class CostDistributionWizard(models.TransientModel):
  _name = 'cost.distribution.wizard'
  _description = 'Cost Distribution Wizard'

  sale_order_id = fields.Many2one('sale.order')
  sale_order_line_id = fields.Many2one('sale.order.line')
  target_line_ids = fields.One2many('cost.distribution.wizard.line', 'wizard_id')

  @api.model
  def default_get(self, fields_list):
    res = super().default_get(fields_list)
    sale_order_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
    if sale_order_line:
      order_lines = sale_order_line.order_id.order_line.filtered(
        lambda l: l.id != sale_order_line.id
      )
    distribution_price = sale_order_line.price_unit * sale_order_line.product_uom_qty
    line_count = len(order_lines)
    if line_count > 0:
      amount_per_line = float_round(distribution_price / line_count if line_count else 0.0, precision_digits=2)
      target_lines_data = [
        (
          0,0,{
                'sale_order_line_id': line.id,
                'amount': amount_per_line,
                'is_selected': True,
              },
        )
        for line in order_lines
      ]
      remainder = distribution_price - (amount_per_line * line_count)
      target_lines_data[0][2]['amount'] += remainder
    else:
      raise UserError("There are no lines to distribute price")
    res.update({
        'sale_order_line_id': sale_order_line.id,
        'target_line_ids': target_lines_data,
    })
    return res

  def distribute_cost_wizard_action(self):
    for record in self:
      if not record.target_line_ids:
        return
      total_shared_amount = sum(record.target_line_ids.mapped("amount"))
      active_sale_order_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
      distributed_sale_price =  active_sale_order_line.price_unit * active_sale_order_line.product_uom_qty
      if total_shared_amount > distributed_sale_price:
        raise ValidationError(f"Total shared amount cannot exceed the original line's price as total share amount is {total_shared_amount} and distributed sale order line's price {distributed_sale_price}")
      active_sale_order_line.division_price = 0.0
      for line in record.target_line_ids:
        line.sale_order_line_id.division_price = line.amount
        line.sale_order_line_id.price_subtotal += line.amount
        line.sale_order_line_id.distributed_line = active_sale_order_line
      active_sale_order_line.division_price = distributed_sale_price - total_shared_amount
      remaining_amount = round(distributed_sale_price - total_shared_amount, 2)
      if remaining_amount > 0:
        active_sale_order_line.division_price = remaining_amount
        active_sale_order_line.price_subtotal = remaining_amount
      else:
        active_sale_order_line.price_subtotal = 0.0


class CostDistributionWizardLine(models.TransientModel):
  _name = 'cost.distribution.wizard.line'
  _description = 'Cost Distribution Wizard Line'

  wizard_id = fields.Many2one('cost.distribution.wizard', string="Wizard")
  sale_order_line_id = fields.Many2one('sale.order.line')
  is_selected = fields.Boolean(string="Selected")
  amount = fields.Float(string="Amount")

  @api.onchange('is_selected', 'wizard_id')
  def _onchange_is_selected(self):
     if not self.is_selected:
      self.amount = 0.0
