from odoo import api, models, fields
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    zero_stock_approval = fields.Boolean(string="Approval")
    show_approval = fields.Boolean(compute="_compute_show_approval")

    def action_confirm(self):
        if not self.zero_stock_approval:
            raise UserError("Can't confirm the order without approval.")

        return super().action_confirm()

    @api.depends_context('uid')
    def _compute_show_approval(self):
        self.show_approval = self.env.user.has_group('sales_team.group_sale_manager')
