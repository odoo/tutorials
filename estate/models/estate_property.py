from odoo import fields, models
from datetime import date
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char('Property Name', required=True, translate=True, default='Unknown')
    availability = fields.Date('Availability Date', required=True, default=lambda self: date.today() + relativedelta(months=3), copy=False)
    address = fields.Char('Address', required=True, translate=True)
    postcode = fields.Char('Postal Code', required=True, translate=True)
    description = fields.Text('Description', translate=True)
    expected_price = fields.Float('Expected Price')
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    living_area = fields.Integer('Living Area')
    bedrooms = fields.Integer('Bedrooms', help='number of bedrooms', default=2)
    facades = fields.Integer('Facades', help='number of facades')
    active = fields.Boolean('Active', default=True)
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')],
        translate=True,
    )
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offerreceived', 'Offer Received'), ('offeraccepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        translate=True,
        default='new',
    )
