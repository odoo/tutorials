import sys
from odoo import models, fields, api

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(required=True, string='Title', trim=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string='Available From', copy=False, default=fields.Date.add(fields.Date.today(),months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False, default=0.0)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
            ])
    total_area = fields.Integer(compute='_compute_total_area', string="Total Area (sqm)")
    state = fields.Selection(selection=[
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], default='new')
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one(comodel_name='estate.property.type', string="Property Type")
    salesperson_id = fields.Many2one(comodel_name='res.users', string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one(comodel_name='res.users', string="Buyer", copy=False)
    tag_ids = fields.Many2many(comodel_name='estate.property.tag', string="Tags")
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id')
    best_price = fields.Float(compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area =  record.living_area + record.garden_area
    
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max((offer.price for offer in record.offer_ids), default=0.0 if not record.offer_ids else None)

    @api.onchange("garden")
    def _onchange_graden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north'if self.garden else None
