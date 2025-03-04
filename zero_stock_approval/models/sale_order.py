# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(string='Approval', copy=False)

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)
        user = self.env.user
        if not user.has_group("sales_team.group_sale_manager"):
            if "zero_stock_approval" in res:
                res["zero_stock_approval"]["readonly"] = True
        return res

    def action_confirm(self):
        for record in self:
            if not record.zero_stock_approval:
                raise UserError(_("You cannot confirm this order without approval. Please contact a Sales Administrator."))
        return super().action_confirm()
