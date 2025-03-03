from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model_create_multi
    def create(self, vals):
        order = self.env['sale.order'].browse(vals[0].get('order_id'))
        line = super().create(vals)
        order._update_deposit_lines()
        return line

    def write(self, vals):
        res = super().write(vals)
        if 'product_uom_qty' in vals or 'product_id' in vals:
            for line in self:
                line.order_id._update_deposit_lines()
        return res

    def unlink(self):
        orders = self.mapped('order_id')
        res = super().unlink()
        for order in orders:
            order._update_deposit_lines()
        return res
