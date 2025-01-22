from odoo import models, fields
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property data model"

    # The name of the property (required field)
    name = fields.Char(required=True)

    # A description for the property
    description = fields.Text()

    # The postcode of the property
    postcode = fields.Char()

    # The availability date for the property, default is 3 months from today
    date_availability = fields.Date(default=fields.Date.today() + relativedelta(months=3))

    # Expected price for the property (required field)
    expected_price = fields.Float(required=True)

    # Selling price of the property (read-only)
    selling_price = fields.Float(readonly=True)

    # Number of bedrooms in the property (default is 2)
    bedrooms = fields.Integer(default=2)

    # The living area of the property (in square meters)
    living_area = fields.Integer()

    # Number of facades (e.g., how many external walls the property has)
    facades = fields.Integer()

    # Whether the property has a garage (True/False)
    garage = fields.Boolean()

    # Whether the property has a garden (True/False)
    garden = fields.Boolean()

    # The area of the garden (in square meters)
    garden_area = fields.Integer()

    # The orientation of the garden (North, South, East, West)
    garden_orientation = fields.Selection(
        selection=[('n', 'North'), ('s', 'South'), ('e', 'East'), ('w', 'West')],
    )

    # Whether the property is active or not (True/False)
    active = fields.Boolean(default=True)

    # The current status of the property (New, Offer Received, etc.)
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                   ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
                   ('cancelled', 'Cancelled')],
        default='new',  # The default state is 'new'
    )
