from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    distributed_cost_tags = fields.Many2many(
        comodel_name='distributed.cost.tag',
        relation='sale_order_line_cost_rel',
        column1='order_line_id',
        column2='tag_id',
        string="Distributed Costs",
    )

    def unlink(self):
        for sale_line in self:
            if sale_line.distributed_cost_tags:
                for cost_tag in sale_line.distributed_cost_tags:
                    if cost_tag.sale_order_line == sale_line:
                        # Find all distributed cost tags related to the current sale order line
                        related_cost_tags = self.env['distributed.cost.tag'].search([
                            ('sale_order_line', '=', sale_line.id)
                        ])
                        for related_tag in related_cost_tags:
                            # Find other sale order lines linked to the same distributed cost tag
                            related_sale_lines = self.env['sale.order.line'].search([
                                ('distributed_cost_tags', '=', related_tag.id),
                                ('id', '!=', sale_line.id)  # Exclude the current sale order line
                            ])
                            related_sale_lines.write({
                                'price_subtotal': related_sale_lines.price_subtotal - float(related_tag.name[1:]),
                            })
                        related_cost_tags.unlink()
                    else:
                        # Adjust related sale order line cost distribution
                        related_sale_line = cost_tag.sale_order_line
                        for related_tag in related_sale_line.distributed_cost_tags:
                            if related_tag.sale_order_line == related_sale_line:
                                new_cost_value = float(related_tag.name[1:]) - float(cost_tag.name[1:])
                                if new_cost_value == 0:
                                    related_tag.unlink()
                                else:
                                    related_tag.write({'name': f"- {new_cost_value:.2f}"})
                        related_sale_line.write({
                            'price_subtotal': related_sale_line.price_subtotal + float(cost_tag.name[1:]),
                        })
        super().unlink()
