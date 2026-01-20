# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    vendor_id = fields.Many2one('res.partner', string="Vendor", domain="[('is_vendor', '=', True)]")
    warehouse_partner_id = fields.Many2one('res.partner', string="Warehouse", domain="[('parent_id', '=', vendor_id), ('type', '=', 'delivery')]")
    is_readonly = fields.Boolean(string="Is readonly", compute="_compute_readonly")

    @api.depends('order_id.vendor_id', 'order_id.warehouse_partner_id')
    def _compute_readonly(self):
        for line in self:
            line.is_readonly = not (line.order_id.vendor_id and line.order_id.warehouse_partner_id)

    @api.onchange('order_id')
    def _onchange_order_id(self):
        self.vendor_id = self.order_id.vendor_id
        self.warehouse_partner_id = self.order_id.warehouse_partner_id

    @api.onchange('vendor_id')
    def _onchange_vendor(self):
        warehouse_partner = self.env["res.partner"].search([("parent_id", "=", self.vendor_id.id), ("type", "=", "delivery")])
        self.warehouse_partner_id = warehouse_partner[0] if warehouse_partner else False;

    @api.onchange('warehouse_partner_id')
    def _onchange_warehouse(self):
        if not self.warehouse_partner_id:
            self.vendor_id = False
