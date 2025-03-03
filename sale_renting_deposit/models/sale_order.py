from odoo import _, api, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("order_line")
    def _onchange_add_product(self):
        if not self.env:
            return
        
        if self.order_line.product_id.requires_deposit:
            deposit_product = self.company_id.deposit_product
            deposit_amount = self.order_line.product_id.deposit_amount

            if not deposit_product:
                self.order_line -= self.order_line[-1]
                raise ValidationError(_("No deposit product? What are we, a charity? 🤣 Go to settings and add one!"))
            else:
                self.order_line += self.env['sale.order.line'].new({
                    'product_id': deposit_product.id,
                    'name': f"Deposit For {self.order_line.product_id.name}",
                    'product_uom_qty': self.order_line.product_uom_qty,
                    'price_unit': deposit_amount,
                    'order_id': self.id
                })

