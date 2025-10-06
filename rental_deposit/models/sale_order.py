from odoo import _, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _add_deposit_product(self, order_line):
        config_product = int(self.env['ir.config_parameter'].sudo().get_param('rental_deposit.deposit_product', default=0))
        if not config_product:
            raise UserError(_("No deposit product configured. Please configure it in Rental Settings."))

        deposit_product = self.env['product.product'].browse(config_product)
        if not deposit_product.exists():
            raise UserError(_("The configured deposit product does not exist."))

        existing_line = self.order_line.filtered(lambda l: l.linked_line_id.id == order_line.id)
        # amount = order_line.product_id.deposit_amount * order_line.product_uom_qty

        if existing_line:
            existing_line.write({
                'product_uom_qty': order_line.product_uom_qty,
                'price_unit': order_line.product_id.deposit_amount,
                'name': f"Deposit for {order_line.product_id.display_name}"
            })
        else:
            self.env['sale.order.line'].create({
                'order_id': self.id,
                'product_id': deposit_product.id,
                'product_uom_qty': order_line.product_uom_qty,
                'product_uom': deposit_product.uom_id.id,
                'price_unit': order_line.product_id.deposit_amount,
                'linked_line_id': order_line.id,
                'name': f"Deposit for {order_line.product_id.display_name}",
            })
