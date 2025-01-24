from odoo import models, fields, api
from odoo.exceptions import UserError

class CostDistributionWizard(models.TransientModel):
    _name = "cost.distribution.wizard"
    _description = "A Wizard to distribute cost over other sales order lines."

    order_line_id = fields.Many2one("sale.order.line", string="Order Line")
    order_line_ids = fields.Many2many("sale.order.line", string="Order Lines")
    order_line_cost = fields.Float(string="Cost to Distribute")
    order_id = fields.Many2one("sale.order")
    price_subtotal = fields.Float("Price Subtotal")

    @api.model
    def default_get(self, fields_list):
        res = super(CostDistributionWizard, self).default_get(fields_list)
        order_id = self.env.context.get("order_id")
        default_order_line_id = self.env.context.get("default_order_line_id")
        default_price_subtotal = self.env.context.get("default_price_subtotal", 0)

        if order_id:
            order = self.env["sale.order"].browse(order_id)
            order_line_ids = order.order_line.ids
            if default_order_line_id in order_line_ids:
                order_line_ids.remove(default_order_line_id)

            res.update({
                "order_id": order_id,
                "order_line_ids": [(6, 0, order_line_ids)],
                "order_line_cost": default_price_subtotal,
            })

            distributed_cost = round(default_price_subtotal / len(order_line_ids), 2) if order_line_ids else 0
            for line in self.env["sale.order.line"].browse(order_line_ids):
                line.write({"distributed_cost": distributed_cost})

        return res

    def distribute_cost(self):
        total_cost_distributed = sum(line.distributed_cost for line in self.order_line_ids)

        if total_cost_distributed > self.price_subtotal:
            raise UserError("Distributed price is greater than the distributable price.")

        for line in self.order_line_ids:
            line.price_subtotal += line.distributed_cost

        original_order_line = self.env["sale.order.line"].browse(self.env.context.get("default_order_line_id"))
        original_order_line.price_subtotal -= total_cost_distributed

        if total_cost_distributed == original_order_line.price_subtotal:
            pass
