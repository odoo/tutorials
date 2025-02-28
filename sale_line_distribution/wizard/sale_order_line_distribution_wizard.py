from random import randint
from odoo import api, Command, fields, models
from odoo.exceptions import UserError


class SaleOrderLineDistributionWizard(models.TransientModel):
    _name = "sale.order.line.distribution.wizard"
    _description = "Sale Order Line Distribution Wizard"

    sale_order_id = fields.Many2one(comodel_name='sale.order', string="Order", required=True)
    distribution_line_ids = fields.One2many(
        comodel_name="sale.order.line.distribution.wizard.line",
        inverse_name="distribution_wizard_id",
        string="Distribution Lines",
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        sale_order_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
        order_lines = sale_order_line.order_id.order_line

        if len(order_lines) == 1:
            raise UserError("The order has only one line.")

        num_distribution_lines = len(order_lines) - 1
        unit_distribution_amount = round(sale_order_line.price_subtotal / num_distribution_lines, 2)
        rounding_adjustment = round((unit_distribution_amount * num_distribution_lines) - sale_order_line.price_subtotal, 2)

        res['distribution_line_ids'] = []
        for target_line in order_lines.filtered(lambda line: line.id != sale_order_line.id):
            allocated_amount = unit_distribution_amount - rounding_adjustment
            res['distribution_line_ids'].append(
                Command.create({
                    'sale_order_line': target_line.id,
                    'distributed_amount': allocated_amount
                })
            )
            
            if rounding_adjustment >= 0.01:
                rounding_adjustment -= 0.01
            elif rounding_adjustment <= -0.01:
                rounding_adjustment += 0.01

        res['sale_order_id'] = sale_order_line.order_id.id
        return res

    def action_apply_distribution(self):
        sale_order_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
        total_distributed_amount = sum(line.distributed_amount for line in self.distribution_line_ids)

        if total_distributed_amount > sale_order_line.price_subtotal:
            raise UserError("The sum of distributed amounts cannot exceed the total cost.")

        tag_color = randint(1, 11)

        for distribution_line in self.distribution_line_ids:
            if distribution_line.distributed_amount:
                cost_tag = self.env['distributed.cost.tag'].create({
                    'name': f"+ {distribution_line.distributed_amount:.2f}",
                    'color': tag_color,
                    'sale_order_line': sale_order_line.id
                })
                distribution_line.sale_order_line.write({
                    'distributed_cost_tags': [(4, cost_tag.id)],
                    'price_subtotal': distribution_line.sale_order_line.price_subtotal + distribution_line.distributed_amount
                })

        if total_distributed_amount > 0:
            negative_cost_tag = self.env['distributed.cost.tag'].create({
                'name': f"-{total_distributed_amount:.2f}",
                'color': tag_color,
                'sale_order_line': sale_order_line.id
            })
            sale_order_line.write({
                'distributed_cost_tags': [(4, negative_cost_tag.id)],
                'price_subtotal': sale_order_line.price_subtotal - total_distributed_amount
            })
