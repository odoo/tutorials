# -*- coding: utf-8 -*-

from odoo import models


class Website(models.Model):
    _inherit = 'website'

    def sale_get_order(self, force_create=False):
        original = super().sale_get_order(force_create)
        if not original:
            return original

        for sale_order in original:
            sale_order_line = sale_order.order_line
            for order in sale_order_line:
                if order.is_deposit_line:
                    product_tmpl_id = order.linked_line_id.product_id.product_tmpl_id.id
                    product_tmpl = self.env['product.template'].browse(product_tmpl_id)
                    order.price_unit = product_tmpl.deposit_amount * order.linked_line_id.product_uom_qty
        return original
