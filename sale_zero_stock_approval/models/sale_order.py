from odoo import fields, models
from odoo.exceptions import AccessError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(string="Approval", default=False)

    def action_confirm(self):
        for record in self:
            for line in record.order_line:
                if (
                    not record.zero_stock_approval
                    and not self.env.user.has_group("sales_team.group_sale_manager")
                    and line.product_id.type == "consu"
                    and line.product_id.is_storable
                    and line.product_id.qty_available < line.product_uom_qty
                ):
                    raise AccessError(
                        "Access denied: You are not authorized to confirm this sales order."
                    )
        return super().action_confirm()
