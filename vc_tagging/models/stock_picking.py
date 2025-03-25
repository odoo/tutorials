# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    vendor_id = fields.Many2one('res.partner', string="Vendor", related="move_ids.sale_line_id.vendor_id", store=True)
    warehouse_partner_id = fields.Many2one('res.partner', string="Warehouse", related="move_ids.sale_line_id.warehouse_partner_id", store=True)
    is_dropshipping = fields.Boolean(string="Is Dropshipping", compute="_compute_is_dropshipping", store=True)

    @api.depends('picking_type_id')
    def _compute_is_dropshipping(self):
        for record in self:
            record.is_dropshipping = record.picking_type_id.code == 'dropship'
