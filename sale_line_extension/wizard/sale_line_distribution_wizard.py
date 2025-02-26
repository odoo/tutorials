from odoo import api, Command ,fields, models


class SaleLineDistributionWizard(models.TransientModel):
    _name = "sale.line.distribution.wizard"
    _description = "Sale Line Distribution Wizard"

    sale_order = fields.Many2one(comodel_name='sale.order', string="Order", required=True)
    order_line_ids = fields.One2many(
        comodel_name="sale.line.distribution.wizard.line", string="Order Lines", inverse_name="wizard_id"
    )
    order_line_cost = fields.Float(string="Cost")
    

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        sale_order_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
        breakpoint()
        order_line_cost = sale_order_line.price_subtotal / len(sale_order_line.order_id.order_line)
        res.update({
            'sale_order': sale_order_line.order_id.id,
            'order_line_ids': [
                Command.create({
                    'order_line': order_line,
                    "distributed_cost": order_line_cost
                    }
                )for order_line in sale_order_line.order_id.order_line 
            ],
        })
        return res
        