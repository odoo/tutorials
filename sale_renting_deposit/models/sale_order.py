from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("order_line")
    def _onchange_add_product(self):
        if not self.env:
            return

        deposit_product = self.company_id.deposit_product
        if not deposit_product:
            return

        self._add_deposit_product(self, deposit_product)

    def _add_deposit_product(self, order, deposit_product):
        existing_rental_products = order.order_line.mapped("product_id")
        removed_deposit_products = order.order_line.filtered(
            lambda line: line.product_id == order.company_id.deposit_product
            and not any(
                f"Deposit For {rental.name}" == line.name
                for rental in existing_rental_products
            )
        )
        order.order_line -= removed_deposit_products

        rental_products = order.order_line.filtered(
            lambda product: product.product_id.requires_deposit
        )
        if rental_products:
            for rental_product in rental_products:
                existing_deposit_product = order.order_line.filtered(
                    lambda line: line.product_id == deposit_product
                    and line.name == f"Deposit For {rental_product.product_id.name}"
                )
                if existing_deposit_product:
                    existing_deposit_product.product_uom_qty = (
                        rental_product.product_uom_qty
                    )
                    existing_deposit_product.price_unit = (
                        rental_product.product_id.deposit_amount
                    )
                else:
                    order.order_line += order.env["sale.order.line"].new(
                        {
                            "product_id": deposit_product.id,
                            "name": f"Deposit For {rental_product.product_id.name}",
                            "product_uom_qty": rental_product.product_uom_qty,
                            "price_unit": rental_product.product_id.deposit_amount,
                            "order_id": order.id,
                        }
                    )
