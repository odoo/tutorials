from odoo import _, api, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("order_line")
    def _onchange_add_product(self):
        if not self.env:
            return
        
        deposit_product = self.company_id.deposit_product
        if not deposit_product:
            return

        existing_rental_products = self.order_line.mapped("product_id")
        removed_deposit_lines = self.order_line.filtered(
            lambda line: line.product_id == self.company_id.deposit_product and 
            not any(f"Deposit For {rental.name}" == line.name for rental in existing_rental_products)
        )
        self.order_line -= removed_deposit_lines

        rental_product_lines = self.order_line.filtered(lambda line: line.product_id.requires_deposit)
        if rental_product_lines:
            for rental_product_line in rental_product_lines:
                existing_deposit = self.order_line.filtered(
                    lambda line: line.product_id == deposit_product and line.name == f"Deposit For {rental_product_line.product_id.name}"
                )
                if not existing_deposit:
                    self.order_line += self.env['sale.order.line'].new({
                        'product_id': deposit_product.id,
                        'name': f"Deposit For {rental_product_line.product_id.name}",
                        'product_uom_qty': rental_product_line.product_uom_qty,
                        'price_unit': rental_product_line.product_id.deposit_amount,
                        'order_id': self.id
                    })
