# -*- coding: utf-8 -*-
from odoo import models, fields, api


class EstateProperty(models.Model):
    _name = 'estate_property'
    _description = 'Real Estate Property'

    def _in_three_months(self):
        return fields.date.today() + fields.date_utils.relativedelta(months=3)

    def _default_salesperson(self):
        return self.env.user
    
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offers_ids.price')
    def _compute_best_price(self):
        for rec in self:
            rec.best_price = max(rec.offers_ids.mapped('price')) or 0.0 

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=_in_three_months
    )

    @api.onchange('date_availability')
    def _onchange_date_availability(self):
        if self.date_availability < fields.date.today():
            return {"warning": {"title": ("Warning"), 
                    "message": ("impossible to set a date prior than today")}}

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

    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None


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
    offers_ids = fields.One2many('estate_property_offer', 'property_id')
    tag_ids = fields.Many2many('estate_property_tags')

    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')


