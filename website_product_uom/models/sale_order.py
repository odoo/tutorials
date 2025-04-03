# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.http import request


class SaleOrder(models.Model):
    _inherit = "sale.order"

    cart_quantity = fields.Float(string="Cart Quantity", compute='_compute_cart_info')

    @api.depends('order_line.product_uom_qty', 'order_line.product_id')
    def _compute_cart_info(self):
        for order in self:
            order.cart_quantity = sum(order.mapped('website_order_line.product_uom_qty'))
            order.only_services = all(sol.product_id.type == 'service' for sol in order.website_order_line)

    def _cart_update(self, product_id, line_id=None, add_qty=0.0, set_qty=0.0, **kwargs):
        """ Add or set product quantity, add_qty can be negative """
        self.ensure_one()
        self = self.with_company(self.company_id)

        if self.state != 'draft':
            request.session.pop('sale_order_id', None)
            request.session.pop('website_sale_cart_quantity', None)
            raise UserError(_('It is forbidden to modify a sales order which is not in draft status.'))

        product = self.env['product.product'].browse(product_id).exists()
        if add_qty and (not product or not product._is_add_to_cart_allowed()):
            raise UserError(_("The given product does not exist therefore it cannot be added to cart."))

        if line_id is not False:
            order_line = self._cart_find_product_line(product_id, line_id, **kwargs)[:1]
        else:
            order_line = self.env['sale.order.line']
        try:
            if add_qty:
                add_qty = float(add_qty)
        except ValueError:
            add_qty = 1
        try:
            if set_qty:
                set_qty = float(set_qty)
        except ValueError:
            set_qty = 0

        quantity = 0
        if set_qty:
            quantity = set_qty
        elif add_qty is not None:
            if order_line:
                quantity = order_line.product_uom_qty + (add_qty or 0)
            else:
                quantity = add_qty or 0

        if quantity > 0:
            quantity, warning = self._verify_updated_quantity(
                order_line,
                product_id,
                quantity,
                **kwargs,
            )
        else:
            # If the line will be removed anyway, there is no need to verify
            # the requested quantity update.
            warning = ''

        order_line = self._cart_update_order_line(product_id, quantity, order_line, **kwargs)

        if (
            order_line
            and order_line.product_template_id.type != 'combo'
            and order_line.price_unit == 0
            and self.website_id.prevent_zero_price_sale
            and product.service_tracking not in self.env['product.template']._get_product_types_allow_zero_price()
        ):
            raise UserError(_("The given product does not have a price therefore it cannot be added to cart."))

        if self.only_services:
            self._remove_delivery_line()
        elif self.carrier_id:
            # Recompute the delivery rate.
            rate = self.carrier_id.rate_shipment(self)
            if rate['success']:
                self.order_line.filtered(lambda line: line.is_delivery).price_unit = rate['price']
            else:
                self._remove_delivery_line()

        return {
            'line_id': order_line.id,
            'quantity': quantity,
            'option_ids': list(set(order_line.linked_line_ids.filtered(
                lambda sol: sol.order_id == order_line.order_id).ids)
            ),
            'warning': warning,
        }
