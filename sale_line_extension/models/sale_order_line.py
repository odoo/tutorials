from odoo import fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    distributed_cost_ids = fields.Many2many(
        comodel_name='distributed.cost.tag',
        relation='sale_order_line_cost_rel',
        column1='order_line_id',
        column2='tag_id',
        string="Distributed Costs",
    )

    def unlink(self):
        for line in self:
            if line.distributed_cost_ids:
                for tag in line.distributed_cost_ids:
                    if tag.sale_order_line == line:
                        pass
                    else:
                        for order_line_tag in tag.sale_order_line.distributed_cost_ids:
                            if order_line_tag.sale_order_line == tag.sale_order_line:
                                changed_name = float(order_line_tag.name[1:]) - float(tag.name[1:])
                                if changed_name == 0:
                                    order_line_tag.unlink()
                                else:
                                    order_line_tag.write({
                                        'name': f"- {changed_name:.2f}",
                                    })
                        tag.sale_order_line.write({
                            'price_subtotal': tag.sale_order_line.price_subtotal+float(tag.name[1:]),
                        })
        super().unlink()
        
