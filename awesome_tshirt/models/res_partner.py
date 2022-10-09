# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    order_ids = fields.One2many('awesome_tshirt.order', 'customer_id', string="Orders")
    has_active_order = fields.Boolean(compute='_compute_has_active_order', store=True)

    @api.depends('order_ids', 'order_ids.state')
    def _compute_has_active_order(self):
        for record in self:
            record.has_active_order = record.order_ids.filtered(lambda r: r.state not in ['sent', 'cancelled'])
