from odoo import models, fields, api
from odoo.osv import expression
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approvalexchttps = fields.Boolean(
        string="Zero Stock Approval",
        help="If enabled, sales users can confirm the order despite zero stock.",
    )

    # Compute the readonly state based on the user's group
    is_zero_stock_readonly = fields.Boolean(
        compute='_compute_is_zero_stock_readonly', 
        string="Is Zero Stock Readonly"
    )

    @api.depends_context('uid')
    def _compute_is_zero_stock_readonly(self):
        """ Check if the user is part of the Sales Manager group """
        is_zero_stock_readonly = self.env.user.has_group('sales_team.group_sale_manager')
        for record in self:
            record.is_zero_stock_readonly = is_zero_stock_readonly


    def action_confirm(self):
        """ Extend the confirmation logic to add approval functionality """
        res = super().action_confirm()
        for order in self:
            if not order.zero_stock_approvalexchttps:
                raise UserError("You can't confirm SO when Zero Stock Blockage disable")
        return res