# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sale_order_id = fields.Many2one('sale.order', string='Source Sales Order')
    warehouse_partner_id = fields.Many2one("res.partner", string="Warehouse")
    is_dropshipping = fields.Boolean(string="Is Dropshipping", compute="_compute_is_dropshipping", store=True)

    @api.depends('sale_order_id')
    def _compute_is_dropshipping(self):
        for order in self:
            order.is_dropshipping = order.sale_order_id
