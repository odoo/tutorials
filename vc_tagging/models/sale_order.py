# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    vendor_id = fields.Many2one("res.partner", string="Vendor", domain="[('is_vendor', '=', True)]")
    warehouse_partner_id = fields.Many2one("res.partner", string="Warehouse", domain="[('parent_id', '=', vendor_id), ('type', '=', 'delivery')]")
           
    @api.onchange('vendor_id', 'warehouse_partner_id')
    def _onchange_vendor_warehouse(self):
        for line in self.order_line:
            line.vendor_id = self.vendor_id
            line.warehouse_partner_id = self.warehouse_partner_id
        
    @api.onchange('vendor_id')
    def _onchange_vendor(self):
        if not self.vendor_id:
            self.warehouse_partner_id = False;
        else:
            warehouse_partner = self.env["res.partner"].search([("parent_id", "=", self.vendor_id.id), ("type", "=", "delivery")])
            self.warehouse_partner_id = warehouse_partner[0] if warehouse_partner else False;

    @api.onchange('warehouse_partner_id')
    def _onchange_warehouse(self):
        if not self.warehouse_partner_id:
            self.vendor_id = False

    def action_confirm(self):  
        """Link confirmed sale orders to corresponding purchase orders by setting the sale_order_id field"""
        res = super().action_confirm()
        for order in self:
            purchase_orders = self.env["purchase.order"].search([("origin", "=", order.name)])
            for po in purchase_orders:
                po.write({"sale_order_id": order.id})
        return res
