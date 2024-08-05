from odoo import fields, models
from datetime import timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(
        string='Availability Date',
        default=lambda self: fields.Date.today() + timedelta(days=90),
        copy=False
    )
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades of Property')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], required=True, default='new', copy=False)
    property_type_id = fields.Many2one(
        'estate.property.type', string="Property")
    buyer_id = fields.Many2one(
        'res.partner', string="Buyer")
    sell_person_id = fields.Many2one(
        'res.users', string="Seller", default=lambda self: self.env.user)
    tag_ids = fields.Many2many(
        'estate.property.tag', string="Tags")
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_id', string='Offers')
