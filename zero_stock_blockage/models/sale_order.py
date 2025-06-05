from odoo import api, models, fields
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(
        string="Zero Stock Approval",
    )

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        fields = super().fields_get(allfields, attributes)
        
        if "zero_stock_approval" in fields:
            fields["zero_stock_approval"]["readonly"] = not self.env.user.has_group("sales_team.group_sale_manager")

        return fields

    def action_confirm(self):
        if not self.env.user.has_group('sales_team.group_sale_manager') and not self.zero_stock_approval:
            for line in self.order_line:
                if line.product_id.qty_available < line.product_uom_qty:
                    raise UserError(
                        "You can not confirm order if any ordered product has insufficient stock. "
                        "If you still want to canform then ask for the zero stock approval permission to manager."
                        )
        return super().action_confirm()
