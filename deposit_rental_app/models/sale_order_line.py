from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_deposit = fields.Boolean(string="Is Deposit", default=False)

    def _handle_deposit_product(self):
        for line in self:
            order = line.order_id

            deposit_product = order.company_id.deposit_product_id

            if not deposit_product:
                continue

            if line.is_deposit or not line.product_id.required_deposit:
                continue

            deposit_amount = line.product_id.amount * line.product_uom_qty

            deposit_line = order.order_line.filtered(
                lambda l: l.is_deposit
                and l.name == f"Deposit for {line.product_id.name}"
            )

            if deposit_amount > 0:
                if deposit_line:
                    deposit_line.with_context(no_update_deposit=True).write(
                        {
                            "price_unit": deposit_amount,
                            "product_uom_qty": 1,
                        }
                    )
                else:
                    order.order_line.with_context(no_update_deposit=True).create(
                        {
                            "order_id": order.id,
                            "product_id": deposit_product.id,
                            "name": f"Deposit for {line.product_id.name}",
                            "price_unit": deposit_amount,
                            "product_uom_qty": 1,
                            "is_deposit": True,
                            "product_uom": deposit_product.uom_id.id,
                        }
                    )
            elif deposit_line:
                deposit_line.unlink()

    @api.model_create_multi
    def create(self, vals_list):
        """Create a product line along with its deposit line"""
        records = super().create(vals_list)
        if not self.env.context.get("no_update_deposit"):
            records._handle_deposit_product()
        return records

    def write(self, vals):
        """Update the product with its deposit line"""
        res = super().write(vals)
        if not self.env.context.get("no_update_deposit"):
            self._handle_deposit_product()
        return res

    @api.ondelete(at_uninstall=False)
    def _unlink_related_deposits(self):
        """Remove deposit lines when the product is removed from recordset"""
        for line in self:
            if line.is_deposit or not line.product_id.required_deposit:
                continue
            deposit_lines = line.order_id.order_line.filtered(
                lambda l: l.is_deposit
                and l.name == f"Deposit for {line.product_id.name}"
            )
        deposit_lines.unlink()
