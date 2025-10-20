from odoo import models, fields
import datetime
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "test description"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Post Code')
    date_availability = fields.Date('Date availability', copy=False, default=datetime.date.today() + relativedelta(months=+3))
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')],
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='state',
        selection=[('new', 'New'),('offerreceived', 'Offer Received'),('offeraccepted', 'Offer Accepted'),('sold', 'Sold'),('cancelled', 'Cancelled')],
    )
