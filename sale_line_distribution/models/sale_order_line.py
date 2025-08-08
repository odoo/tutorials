from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    distributed_cost_tags = fields.Many2many(
        comodel_name='distributed.cost.tag',
        relation='sale_order_line_cost_rel',
        column1='order_line_id',
        column2='tag_id',
        string="Distributed Costs",
        ondelete='cascade'
    )

    def unlink(self):
        for sale_line in self:
            if sale_line.distributed_cost_tags:
                for cost_tag in sale_line.distributed_cost_tags:
                    if cost_tag.parent_tag:
                        cost_tag.sale_order_line.write({
                            'price_subtotal': cost_tag.sale_order_line.price_subtotal - float(cost_tag.name[1:])
                        })
                        cost_tag.parent_tag.sale_order_line.write({
                            'price_subtotal': cost_tag.parent_tag.sale_order_line.price_subtotal + float(cost_tag.name[1:])
                        })
                        new_cost_value = float(cost_tag.parent_tag.name[1:]) - float(cost_tag.name[1:])
                        cost_tag.parent_tag.write({'name': f"- {new_cost_value:.2f}"})
                        cost_tag.unlink()
                    else:
                        for child_tag in cost_tag.child_tags:
                            child_tag.sale_order_line.write({
                                'price_subtotal': child_tag.sale_order_line.price_subtotal - float(child_tag.name[1:])
                            })
                        cost_tag.child_tags.unlink()
        super().unlink()
