# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warranty_linked_with_product_id = fields.Many2one("sale.order.line", ondelete="cascade")
    warranty_id = fields.Many2one('product.warranty', string="Warranty")
