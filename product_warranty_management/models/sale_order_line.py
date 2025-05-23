# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, _, api, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
     
    @api.depends('product_id', 'state', 'qty_invoiced', 'qty_delivered')
    def _compute_product_updatable(self):
        super()._compute_product_updatable()
        for order_line in self:
            if order_line.linked_line_ids:
                order_line.product_updatable = False
        return
