from odoo import models, fields


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate property model'

#   Property information
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode', required=True)
    date_availability = fields.Date('Availability', copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    has_garage = fields.Boolean('Garage')
    has_garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'),
                   ('south', 'South'),
                   ('east', 'East'),
                   ('west', 'West'),
        ]
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'),
                   ('offer_received', 'Offer Received'),
                   ('offer_accepted', 'Offer accepted'),
                   ('sold', 'Sold'),
                   ('cancelled', 'Cancelled'),
        ],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type", string='Property Type')

#   Other Information
    salesman_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)

#   Tags
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')

#   Offers
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offer')
