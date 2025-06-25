from odoo import fields, models, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    zero_stock_approval = fields.Boolean(string="Approval", default="false")

    def action_confirm(self):
        result = super().action_confirm()
        for order in self:
            if not order.zero_stock_approval:
                raise UserError(
                    "This sale order cannot be confirmed without zero stock approval"
                )
        return result

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)
        if not self.env.user.has_group("sales_team.group_sale_manager"):
            if "zero_stock_approval" in res:
                res["zero_stock_approval"]["readonly"] = True
        return res
