import datetime

from odoo import models, fields


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'name desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Available From',
                                    default=fields.Datetime.today() + datetime.timedelta(
                                        days=90))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    bathrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean(default=False)
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    temp = fields.Char()
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer received', 'Offer Received'),
        ('offer accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], required=True, default='new', copy=False)
    property_type_id = fields.Many2one('estate.property.type',
                                       string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    salesperson_id = fields.Many2one('res.users', string='Salesman',
                                     default=lambda self: self.env.user)
    tags_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(required=True)


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(required=True)


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    property_id = fields.Many2one('estate.property', required=True)
    partner_id = fields.Many2one('res.partner', required=True)
    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)
