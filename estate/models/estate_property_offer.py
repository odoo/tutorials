# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Estate Property Offer"
    _order = "sequence"

    price = fields.Float('price')
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate_property', string='Property', required=True)
    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence', default=10)

