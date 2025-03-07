from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_is_kit = fields.Boolean(related='product_template_id.is_kit', string="Is Kit")
    product_state = fields.Selection(related='order_id.state', string="Product Status")

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_price_unit(self):
        """Price unit calculation for Kit and Regular products."""
        kit_prices = {order_line.id: order_line.price_unit for order_line in self if order_line.product_is_kit}

        super()._compute_price_unit()

        for line in self.filtered(lambda order_line: order_line.product_is_kit and order_line.product_id):
            line.price_unit = kit_prices.get(line.id, line.price_unit)
