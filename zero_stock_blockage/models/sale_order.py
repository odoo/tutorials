from odoo import api, models, fields, exceptions


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    zero_stock_approval = fields.Boolean(
        string="Approval",
        help="Allow users to confirm sale order on zero stock availability")

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)

        if not self.env.user.has_group("sales_team.group_sale_manager"):
            if "zero_stock_approval" in res:
                res["zero_stock_approval"]["readonly"] = True
        return res

    def action_confirm(self):
        if not self.env.user.has_group("sales_team.group_sale_manager"):
            for order in self:
                if not order.zero_stock_approval:
                    for line in order.order_line:
                        product = line.product_id
                        if product.type == 'consu' and product.qty_available < line.product_uom_qty:
                            raise exceptions.UserError(
                                ("You cannot confirm this Sale Order because the product '%s' has insufficient stock.\n"
                                " Available: %s, Required: %s") %
                                (product.display_name, product.qty_available, line.product_uom_qty)
                            )
        return super().action_confirm()
