from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(
        string="Approval",
        copy=False,
    )

    @api.onchange('zero_stock_approval')
    def _onchange_zero_stock_approval(self):
        if self.zero_stock_approval and self.env.user.has_group('sales_team.group_sale_manager'):
            warnings = []
            for line in self.order_line:
                if line.product_id.type == 'consu' and line.product_uom_qty > line.product_id.qty_available:
                    warnings.append(
                        f"Product '{line.product_id.display_name}' has demand {line.product_uom_qty} > available {line.product_id.qty_available}."
                    )
            if warnings:
                return {
                    'warning': {
                        'title': "Heads Up – Stock Alert ⚠️",
                        'message': (
                            "You're approving an order where some products have lower available stock than requested quantity:\n\n"
                            + "\n".join(warnings) +
                            "\n\nIf you're sure about this decision, you can continue. Otherwise, consider adjusting the quantities or stock."
                        )
                    }
                }

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        fields = super().fields_get(allfields=allfields, attributes=attributes)
        if not self.env.user.has_group('sales_team.group_sale_manager'):
            if "zero_stock_approval" in fields:
                fields['zero_stock_approval']['readonly'] = True
        return fields

    def action_confirm(self):
        for order in self:
            stock_issues = []

            for line in order.order_line:
                demand_qty = line.product_uom_qty
                available_qty = line.product_id.qty_available

                # if demand_qty <= 0:
                #         raise UserError(
                #         f"You cannot confirm this Sale Order.\n"
                #         f"Product '{line.product_id.display_name}' has a quantity of {demand_qty}.\n"
                #         f"Quantity must be greater than zero."
                # )

                if (
                    line.product_id.type == 'consu'
                    and demand_qty > available_qty
                    and not self.env.user.has_group('sales_team.group_sale_manager')
                    and not order.zero_stock_approval
                ):
                    stock_issues.append(
                        f"- {line.product_id.display_name}: Requested {demand_qty}, Available {available_qty}"
                    )

            if stock_issues:
                raise UserError(
                    "Cannot confirm this Sale Order due to insufficient stock:\n\n" +
                    "\n".join(stock_issues) +
                    "\n\nPlease get approval or adjust the quantities."
                )

        return super().action_confirm()
