# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit="account.move.line"

    @api.onchange('sale_line_ids')
    def _onchange_sale_line(self):
        for line in self:
            if line.sale_line_ids:
                if line.sale_line_ids.order_id and line.sale_line_ids.order_id.invoice_policy == 'order':
                    line.quantity = line.sale_line_ids.s_quantity
