# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'
     
    @api.onchange('order_line')
    def _onchange_order_line(self):
        modified_order_lines = self._origin.order_line.filtered(
            lambda line: line.id not in self.order_line.ids
        )
        if len(modified_order_lines) > 0:
            list_of_linked_line_ids = modified_order_lines.mapped('linked_line_ids').ids
            self.order_line = [Command.delete(id) for id in list_of_linked_line_ids]
        return super()._onchange_order_line()
