from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    source_order_line_id = fields.Many2one(comodel_name='sale.order.line', string='Source Order Line')

    def unlink(self):
        to_unlink = self.env['sale.order.line'].search([("source_order_line_id", "in", self.ids)]).filtered(lambda wl: wl not in self)
        if to_unlink:
            to_unlink.unlink()

        return super().unlink()
