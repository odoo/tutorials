from odoo import fields, models
from odoo.exceptions import AccessError


class SaleZeroStock(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(string="Approval by Manager", default=False)

    def action_confirm(self):
        for record in self:
            for item in record.order_line:
                if (
                    not record.zero_stock_approval
                    and not self.env.user.has_group("sales_team.group_sale_manager")
                    and item.product_id.type == "consu"
                    and item.product_id.is_storable
                    and item.product_id.qty_available < item.product_uom_qty
                ):
                    raise AccessError(
                        "Access denied: You are not allowed to confirm this sales order."
                    )
        return super().action_confirm()
