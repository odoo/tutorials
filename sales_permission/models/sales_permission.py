from odoo import models, fields 
from odoo.exceptions import UserError

class SalesOrderConformPermission(models.Model):
    _inherit = "sale.order"

    zero_stock_approval = fields.Boolean(string="Zero Stock Approval")

    def action_confirm(self):
        if self.zero_stock_approval or self.env.user.has_group('sales_team.group_sale_manager'):
            return super().action_confirm()
        else:
            raise UserError("You Have Not Rights to Confirm this order !!!!!")
