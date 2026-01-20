# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(string="Approval", copy=False)

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)
        if 'zero_stock_approval' in res and not self.env.user.has_group('sales_team.group_sale_manager'):
                res['zero_stock_approval']['readonly'] = True
        return res

    def action_confirm(self):
        if not self.zero_stock_approval:
            raise UserError(_("Cannot confirm a quotation without approval from manager."))
        return super().action_confirm()
