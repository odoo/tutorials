from odoo.exceptions import UserError

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(
        string="Approval",
        help="Order Approval by manager,\nif order has insufficient stock then this approval is required by manager.",
        copy=False,
    )

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)
        if not self.env.user.has_group("sales_team.group_sale_manager"):
            if "zero_stock_approval" in res:
                res["zero_stock_approval"]["readonly"] = True
        return res

    def action_confirm(self):
        for record in self:
            if not record.order_line:
                raise UserError("You cannot confirm a Quotation without any products.")
            if record.zero_stock_approval:
                return super().action_confirm()
            for line in record.order_line:
                if (
                    line.product_id.qty_available < line.product_uom_qty
                    and line.product_id.type == "consu"
                    and not record.zero_stock_approval
                    and not self.env.user.has_group("sales_team.group_sale_manager")
                ):
                    raise UserError(
                        "Cannot confirm this Sale Order due to insufficient stock.\n\nPlease get approval or adjust the quantities."
                    )
        return super().action_confirm()
