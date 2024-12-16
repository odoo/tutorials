# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Manage different offers from buyers for a specific property."

    price = fields.Float(string="Price", required=True)

    status = fields.Selection([('accepted', 'Accepted'),
                               ('refused', 'Refused')],
                               copy=False)

    partner_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        required=True
    )

    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True
    )