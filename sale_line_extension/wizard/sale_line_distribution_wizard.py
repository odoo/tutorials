from random import randint
from odoo import api, Command ,fields, models
from odoo.exceptions import UserError


class SaleLineDistributionWizard(models.TransientModel):
    _name = "sale.line.distribution.wizard"
    _description = "Sale Line Distribution Wizard"

    sale_order = fields.Many2one(comodel_name='sale.order', string="Order", required=True)
    distribution_line_ids = fields.One2many(
        comodel_name="sale.line.distribution.wizard.line", string="Order Lines", inverse_name="wizard_id",
    )
    
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        sale_order_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
        if len(sale_order_line.order_id.order_line) == 1:
            raise UserError("The order has only one line.")
        distribution_line_cost = round(sale_order_line.price_subtotal / (len(sale_order_line.order_id.order_line)-1),2)
        difference = round((distribution_line_cost * (len(sale_order_line.order_id.order_line)-1)) - sale_order_line.price_subtotal, 2)
        res['distribution_line_ids'] = []
        for sale_order_line in sale_order_line.order_id.order_line.filtered(lambda line:
            line.id != sale_order_line.id):

            res['distribution_line_ids'].append(
                Command.create({
                    'sale_order_line': sale_order_line.id,
                    "distributed_cost": distribution_line_cost - difference
                })
            )
            if difference >= 0.01:
                difference = difference - 0.01
            elif difference <= -0.01:
                difference = difference + 0.01
        res['sale_order'] = sale_order_line.order_id.id
        return res

    def action_divide(self):
        sale_order_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
        total_cost = sum(line.distributed_cost for line in self.distribution_line_ids)

        if total_cost > sale_order_line.price_subtotal:
            raise UserError("The sum of distributed costs cannot exceed the total cost.")
        color = randint(1, 11)

        for line in self.distribution_line_ids:
            if line.distributed_cost != 0:
                cost_tag = self.env['distributed.cost.tag'].create({
                    'name': f"+ {line.distributed_cost:.2f} ",
                    'color': color,
                    'sale_order_line': sale_order_line.id
                })
                line.sale_order_line.write({
                    'distributed_cost_ids': [(4, cost_tag.id)],
                    'price_subtotal': line.sale_order_line.price_subtotal+line.distributed_cost
                })

        if total_cost > 0:
            negative_cost_tag = self.env['distributed.cost.tag'].create({
                'name': f"-{total_cost:.2f}",
                'color': color,
                'sale_order_line': sale_order_line.id
            })
            sale_order_line.write({
                'distributed_cost_ids': [(4, negative_cost_tag.id)],
                'price_subtotal': sale_order_line.price_subtotal-total_cost
            })
