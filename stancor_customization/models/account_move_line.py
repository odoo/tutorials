# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit="account.move.line"

    @api.onchange('sale_line_ids')
    def _onchange_sale_line(self):
        if self.sale_line_ids:
            if self.sale_line_ids.order_id and self.sale_line_ids.order_id.invoice_policy == 'order':
                self.quantity = self.sale_line_ids.s_quantity
