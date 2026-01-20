# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _make_po_get_domain(self, company_id, values, partner):
        """Modify the purchase order domain to ensure the correct vendor is selected based on the sale order line."""
        domain = super()._make_po_get_domain(company_id, values, partner)
        sale_line_id = values.get('sale_line_id') if values else False
        if sale_line_id:
            sale_order_line = self.env['sale.order.line'].browse(sale_line_id)
            if sale_order_line and sale_order_line.vendor_id:
                domain = list(domain)
                domain[0] = ('partner_id', '=', sale_order_line.vendor_id.id)
        return tuple(domain)

    def _prepare_purchase_order(self, company_id, origins, values):
        """Prepare purchase order with vendor and warehouse details based on the sale order line."""
        res = super()._prepare_purchase_order(company_id, origins, values)
        sale_line_id = values[0].get('sale_line_id') if values else False
        if sale_line_id:
            sale_order_line = self.env['sale.order.line'].browse(sale_line_id)
            if sale_order_line and sale_order_line.vendor_id:
                res.update({
                    'partner_id': sale_order_line.vendor_id.id,
                    'warehouse_partner_id': sale_order_line.warehouse_partner_id.id
                })
        return res
