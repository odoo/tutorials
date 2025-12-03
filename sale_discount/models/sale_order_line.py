from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('price_unit', 'product_uom_qty', 'discount')
    def _onchange_recalc_discount(self):
        if self.order_id:
            self.order_id._onchange_recalculate_global_discount()
