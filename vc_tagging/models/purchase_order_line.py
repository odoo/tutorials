# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.model
    def _prepare_purchase_order_line(self, product_id, product_qty, product_uom, company_id, supplier, po):
        """Prepare purchase order line with vendor-specific pricing if available."""
        values = super()._prepare_purchase_order_line(product_id, product_qty, product_uom, company_id, supplier, po)

        vendor = next((supplier for supplier in product_id.seller_ids if supplier.partner_id == po.partner_id), None)
        values['price_unit'] = vendor.price if vendor else product_id.standard_price

        return values
