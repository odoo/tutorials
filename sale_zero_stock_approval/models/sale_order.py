from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(
        string="Approval",
        copy=False
    )

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)
        if not self.env.user.has_group("sales_team.group_sale_manager") and "zero_stock_approval" in res:
                res["zero_stock_approval"]["readonly"] = True
        return res

    def action_confirm(self):
        if not self.zero_stock_approval and not self.env.user.has_group('sales_team.group_sale_manager'):
            raise UserError(_('Sales order cannot be confirmed unless it is approved'))

        return super().action_confirm()
