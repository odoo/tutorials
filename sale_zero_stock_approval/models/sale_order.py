# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(string='Approval', copy=False)

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)
        if not self.env.user.has_group('sales_team.group_sale_manager'):
            if 'zero_stock_approval' in res:
                res['zero_stock_approval']['readonly'] = True
        return res

    def action_confirm(self):
        for order in self:
            has_zero_stock = False
            for line in order.order_line:
                if line.product_uom_qty <= 0:
                    has_zero_stock = True
                    break
            if has_zero_stock and not order.zero_stock_approval:
                raise UserError(_('Cannot confirm order with zero stock products without approval.'))
        return super().action_confirm()
