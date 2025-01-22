# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, fields, models


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate properties model'

    name = fields.Char('Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    property_type_id = fields.Many2one('estate.property.type')
    tag_ids = fields.Many2many('estate.property.tag')

    date_availability = fields.Date('Available From')
    expected_price = fields.Float(required=True)
    best_offer = fields.Float(compute='_compute_best_offer')
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
    state = fields.Selection(string='Status', required=True, default='new', readonly=True, selection=[
        ('new', 'New'),
        ('offer_received', 'Offer received'),
        ('offer_accepted', 'Offer accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ])
    buyer_id = fields.Many2one('res.partner', readonly=True)
    user_id = fields.Many2one(
        'res.users', string='Salesperson', default=lambda self: self.env.user)
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_id', string='Offers')

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

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError(
                    'Sold properties can not be cancelled')
            record.state = 'cancelled'
        return True

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError(
                    'Cancelled properties can not be sold')
            record.state = 'sold'
        return True
