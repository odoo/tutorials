from odoo import fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Property(models.Model):

    # Model definition
    _name = "estate.property"
    _description = "Estate Property"

    # Fields
    name = fields.Char('Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        'Available From',
        default=datetime.today() + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        copy=False,
        default='new',
    )
