from odoo import models, fields
from datetime import date
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "test"

    name = fields.Char(string='Name', required=True)
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Date available', copy=False, default=(date.today() + relativedelta(months=3)))
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedroom', default=2)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facade')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Direction of the garden")
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        help='state of the proerty right now',
        required=True,
        copy=False,
        default='new')
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type',
        help='Type of the property'
    )
    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False,
        help='Buyer of the property'
    )
    seller_id = fields.Many2one(
        'res.users',
        string='Seller',
        default=lambda self: self.env.user,
        help='Seller of the property'
    )
    tag_ids = fields.Many2many(
        'estate.property.tag',
        string='Tags',
        help='Tags associated with the property'
    )
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers',
    )
