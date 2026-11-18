from odoo import _, fields, models
from odoo.exceptions import AccessError
from odoo.tools.float_utils import float_compare


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zero_stock_approval = fields.Boolean(
        string='Approval',
        copy=False,
    )
    has_access_zero_stock_approval = fields.Boolean(
        compute='_compute_hash_access',
    )

    def _compute_hash_access(self):
        has_access = self.env.user.has_group('sales_team.group_sale_manager')
        for order in self:
            order.has_access_zero_stock_approval = has_access

    def write(self, vals):
        if 'zero_stock_approval' in vals:
            if not self.env.user.has_group(
                    'sales_team.group_sale_manager'
            ):
                raise AccessError(
                    _("Only Sales Administrators can modify this field.")
                )
        return super().write(vals)

    def _confirmation_error_message(self):
        self.ensure_one()

        error = super()._confirmation_error_message()
        if error:
            return error

        if not self.order_line:
            return _("Please add at least one order line.")

        for line in self.order_line:
            if line.display_type or line.is_downpayment:
                continue

            product = line.product_id

            if not product.is_storable:
                continue

            available_qty = product.with_context(
                warehouse=self.warehouse_id.id
            ).free_qty

            ordered_qty = line.product_uom_id._compute_quantity(
                line.product_uom_qty,
                product.uom_id,
            )

            if float_compare(
                    ordered_qty,
                    available_qty,
                    precision_rounding=product.uom_id.rounding,
            ) > 0 and not self.zero_stock_approval:
                return _(
                    "Zero Stock Approval is required to confirm this order "
                    "because the requested quantity exceeds available stock."
                )

        return False
