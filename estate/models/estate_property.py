# -*- coding: utf-8 -*-
from odoo import models, fields


class EstateProperty(models.Model):
    _name = 'estate_property'
    _description = 'Real Estate Property'

    def _in_three_months(self):
        return fields.date.today() + fields.date_utils.relativedelta(months=3)

    def _default_salesperson(self):
        return self.env.user

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=_in_three_months
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False) 
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], default='new', copy=False)

    property_type_id = fields.Many2one(
        'estate_property_type',
        string='Property Type'
    )
    buyer = fields.Many2one('res.partner', copy=False)
    salesperson = fields.Many2one('res.users', default=_default_salesperson)
