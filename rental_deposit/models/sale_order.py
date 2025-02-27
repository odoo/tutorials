from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line')
    def _onchange_add_product(self):
        self._manage_deposit_lines()

    def _manage_deposit_lines(self):
        deposit_product_id = self.company_id.deposit_product_id
        if not deposit_product_id:
            return

        for line in self.order_line:
            if line.product_id.requires_deposit:

                exisiting_deposit_lines = self.order_line.filtered(
                    lambda l: l.name == f"Deposit for {line.product_id.name}",
                )

                if not exisiting_deposit_lines:
                    self.order_line += self.env['sale.order.line'].new({
                        'order_id': self.id,
                        'product_id': deposit_product_id.id,
                        'name': f"Deposit for {line.product_id.name}",
                        'deposit_parent_product_id': line.product_id.id,
                        'product_uom_qty': line.product_uom_qty,
                        'price_unit': line.product_id.deposit_amount,
                    })
                else:
                    exisiting_deposit_lines.write({
                        'product_uom_qty': line.product_uom_qty,
                        'price_unit':line.product_id.deposit_amount,
                    })
