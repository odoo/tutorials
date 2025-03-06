from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _update_deposit_product(self):
        for order in self:
            deposit_product = order.company_id.deposit
            if not deposit_product:
                continue

            total_deposit_amount = sum(
                line.product_id.amount * line.product_uom_qty
                for line in order.order_line.filtered(
                    lambda l: not l.is_deposit and l.product_id.require_deposit
                )
            )
            deposit_line = order.order_line.filtered(
                lambda l: l.is_deposit and l.product_id == deposit_product
            )

            if total_deposit_amount > 0:
                if deposit_line:
                    deposit_line.with_context(no_update_deposit=True).write(
                        {"price_unit": total_deposit_amount}
                    )
                else:
                    order.with_context(no_update_deposit=True).update(
                        {
                            "order_line": [
                                (
                                    0,
                                    0,
                                    {
                                        "product_id": deposit_product.id,
                                        "name": f"Added for {order.order_line.name}",
                                        "price_unit": total_deposit_amount,
                                        "product_uom_qty": 1,
                                        "is_deposit": True,
                                    },
                                )
                            ]
                        }
                    )
            elif deposit_line:
                deposit_line.unlink()
