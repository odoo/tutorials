from odoo import fields, models
from odoo.exceptions import AccessError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(
        string='Approval',
        copy=False,
    )
    has_access_zero_stock_approval = fields.Boolean(
        compute='_compute_hash_access',
    )

    def _compute_hash_access(self):
        has_access = self.env.user.has_group('sales_team.group_sale_manager')
        for order in self:
            order.has_access_zero_stock_approval = has_access

    def write(self, vals):
        if 'zero_stock_approval' in vals:
            if not self.env.user.has_group(
                    'sales_team.group_sale_manager'
            ):
                raise AccessError(
                    self.env._("Only Sales Administrators can modify this field.")
                )
        return super().write(vals)
