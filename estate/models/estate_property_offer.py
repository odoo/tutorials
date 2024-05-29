# -*- coding: utf-8 -*-

from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = 'estate_property_offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ])

    partner_id = fields.Many2one('res.partner')
    property_id = fields.Many2one('estate_property')