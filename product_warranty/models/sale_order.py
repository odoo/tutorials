from odoo import fields, models, api, Command

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('order_line')
    def _onchange_order_line(self):
        super(SaleOrder,self)._onchange_order_line()
        a = []
        for line in self.order_line:
            if line.linked_line_id.id and line.linked_line_id.id not in self.order_line.ids:
                a.append(line.linked_line_id.id)
        hy = self.order_line.search([('linked_line_id', 'in', a)])
        self.order_line = [Command.delete(h) for h in hy.ids]
