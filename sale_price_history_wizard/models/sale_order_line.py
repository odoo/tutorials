# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        related="order_id.partner_id",
        store=True
    )
