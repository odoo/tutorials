# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate properties model'

    name = fields.Char('Title', required=True)
    description = fields.Text()
    postcode = fields.Char()

    date_availability = fields.Date('Available From')
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(default=0.0, readonly=True)

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
    total_area = fields.Integer(
        'Total Area (m²)', compute='_compute_total_area')
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
    best_offer = fields.Float(compute='_compute_best_offer')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.mapped(
                'offer_ids.price'), default=0.0)
