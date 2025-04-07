# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _prepare_account_move_line(self, move=False):
        res = super()._prepare_account_move_line(move=move)
        if self.env.context.get('to_invoice_line_ids') and self.id not in self.env.context.get('to_invoice_line_ids'):
            return False
        return res
