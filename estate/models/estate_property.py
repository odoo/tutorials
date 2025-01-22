# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate properties model'

    name = fields.Char('Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Available From')
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer('Living Area (m²)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden Area (m²)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('east', 'East'),
            ('south', 'South'),
            ('west', 'West')
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(string='Status', required=True, default='new', selection=[
        ('new', 'New'),
        ('offer_received', 'Offer received'),
        ('offer_accepted', 'Offer accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ])
    property_type_id = fields.Many2one('estate.property.type')
    buyer_id = fields.Many2one('res.partner')
    user_id = fields.Many2one(
        'res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_id', string='Offers')
