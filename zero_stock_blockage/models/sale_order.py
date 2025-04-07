from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approvalexchttps = fields.Boolean(string="Approval", default=False)

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            if not order.zero_stock_approvalexchttps:
                raise ValidationError("Please check for approval to confirm SO")
        return res

    readonly_status = fields.Boolean(
        compute='_compute_readonly_status',
        string="Zero Stock Approval Status"
    )

    @api.depends_context('uid')
    def _compute_readonly_status(self):
        readonly_status = self.env.user.has_group('sales_team.group_sale_manager')
        for record in self:
            record.readonly_status = readonly_status
