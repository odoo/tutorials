# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
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
        # Loop through each order in the recordset
        for order in self:
            # Loop through each order line in the order
            if any(line.product_uom_qty <= 0 for line in order.order_line):
                if not order.zero_stock_approval:
                    raise UserError(_('Approval is required to confirm an order containing products with zero stock.'))
        return super().action_confirm()
