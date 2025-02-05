from odoo import fields, models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    # Basic fields for property details
    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Availability Date",
        default=lambda self: fields.Date.today() + relativedelta(months=3)  
    )
    expected_price = fields.Float(string="Expected Price", required=True, default=0.0)
    selling_price = fields.Float(string="Selling Price", readonly=True)  
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sq.m.)")
    facades = fields.Integer(default=3)
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden")
    garden_area = fields.Integer(string="Garden Area (sq.m.)")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('new', 'new'),
        ('offer received','offer received'),
        ('east', 'East'),
        ('west', 'West')
    ], string='Garden Orientation')

    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default='new',
        required=True,
        copy=False,
     )
    active = fields.Boolean(default=True)  