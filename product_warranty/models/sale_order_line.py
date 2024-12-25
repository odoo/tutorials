from odoo import fields, models, api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warranty_id = fields.Many2one('sale.order.line', ondelete="cascade")

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('order_line')
    def _onchange_order_line(self):
        super(SaleOrder,self)._onchange_order_line()
        for line in self.order_line:
            if line.warranty_id:
                line.warranty_id.unlink()
                break
