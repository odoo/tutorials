from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(string='Approval', default=False, copy=False)

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)
        if not self.env.user.has_group('sales_team.group_sale_manager'):
            if 'zero_stock_approval' in res:
                res['zero_stock_approval']['readonly'] = True
        return res

    def action_confirm(self):
        for order in self:
            if not order.zero_stock_approval:

                if not order.order_line:
                    raise UserError(_("Can't confirm empty order without approval"))

                for line in order.order_line:
                    if line.product_id.qty_available <= 0:
                        raise UserError(_("Can't confirm order with zero stock products without approval"))

        return super().action_confirm()
