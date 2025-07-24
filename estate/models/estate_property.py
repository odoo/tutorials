from odoo import models, fields
from datetime import date
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    # Title of the property (required)
    name = fields.Char(string='Title', required=True)

    # Detailed description text
    description = fields.Text(string='Description')

    # Postcode as a simple Char field
    postcode = fields.Char(string='Postcode')

    # Availability date with default 3 months from today; copy=False avoids duplication on record duplication
    date_availability = fields.Date(
        string='Availability From',
        copy=False,
        default=(date.today() + relativedelta(months=3))
    )

    # Expected sale price (required)
    expected_price = fields.Float(string='Expected Price', required=True)

    # Actual selling price, read-only (set by system or workflow), not copied on duplication
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)

    # Number of bedrooms with default value
    bedrooms = fields.Integer(string='Bedrooms', default=2)

    # Living area in square meters
    living_area = fields.Integer(string='Living Area (sqm)')

    # Number of facades
    facades = fields.Integer(string='Facades')

    # Garage capacity count
    garage = fields.Integer(string='Garage')

    # Boolean indicating if garden exists
    garden = fields.Boolean(string='Garden')

    # Garden area in square meters
    garden_area = fields.Integer(string='Garden Area (sqm)')

    # Orientation of the garden with default 'north'
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string='Garden Orientation',
        default='north'
    )

    # Status of the property; required, default 'new', not copied on duplication
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        required=True,
        copy=False,
        default='new'
    )

    # Active flag to archive/unarchive records easily
    active = fields.Boolean(string='Active', default=True)
