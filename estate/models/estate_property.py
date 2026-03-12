from dateutil.relativedelta import relativedelta
from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string='Property Name', required=True, help='Enter the name of the property')
    description = fields.Text(string='Property Description', help='Enter a description of the property')
    postcode = fields.Char(string='Postcode', help='Enter the postcode of the property')
    date_availability = fields.Date(string='Availability Date', help='Enter the date when the property becomes available', copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string='Expected Price', required=True, help='Enter the expected price of the property')
    selling_price = fields.Float(string='Selling Price', help='Enter the selling price of the property', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Number of Bedrooms', help='Enter the number of bedrooms in the property', default=2)
    living_area = fields.Integer(string='Living Area', help='Enter the living area of the property in square meters')
    facades = fields.Integer(string='Number of Facades', help='Enter the number of facades of the property')
    garage = fields.Boolean(string='Garage', help='Check if the property has a garage')
    garden = fields.Boolean(string='Garden', help='Check if the property has a garden')
    garden_area = fields.Integer(string='Garden Area', help='Enter the area of the garden in square meters')
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string='Garden Orientation',
        help='Select the orientation of the garden'
    )
    active = fields.Boolean(string='Active', default=True, help='Set to False to archive the property')
    state = fields.Selection(
        selection=[
            ('new', 'New Offer'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        string='Status',
        required=True,
        copy=False,
        default='new',
        help='Current status of the property'
    )
