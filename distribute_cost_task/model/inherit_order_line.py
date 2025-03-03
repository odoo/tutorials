from odoo import api, fields, models


class InheritOrderLine(models.Model):
    _inherit = "sale.order.line"

    divide_cost = fields.Float("Devision")
    divide_to_order_lines = fields.One2many("order.line.cost.divide", "divide_to_order_line", string="Divided to order line")
    divide_from_order_lines = fields.One2many("order.line.cost.divide", "divide_from_order_line", string="Divided from order line")

    def action_open_order_line_wizard(self):
        return {
            "name": "Order Line Wizard",
            "type": "ir.actions.act_window",
            "res_model": "order.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "order_id": self.order_id.id,
            },
        }

    @api.ondelete(at_uninstall=False)
    def _divide_cost(self):
        for record in self:
            for line in record.divide_to_order_lines:
                line.divide_from_order_line.divide_cost += line.cost
                line.cost = 0.0
            for line in record.divide_from_order_lines:
                line.divide_to_order_line.divide_cost -= line.cost 
                line.cost = 0.0       

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'divide_cost')
    def _compute_amount(self):
        super(InheritOrderLine, self)._compute_amount() 
        for record in self:
            if record.divide_from_order_lines:
                record.price_subtotal -= record.price_unit
                record.price_subtotal += record.divide_cost
            else:
                record.price_subtotal += record.divide_cost
