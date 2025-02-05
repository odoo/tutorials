from odoo import fields, models
from datetime import timedelta
from datetime import datetime

class realEstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate property table :)"

    id = fields.Integer()
    create_uid = fields.Integer()
    create_date = fields.Datetime('Create Date', readonly=True, default=fields.Datetime.now)
    write_uid = fields.Integer()
    write_date = fields.Datetime('Write Date', readonly=True, default=fields.Datetime.now)
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date availability',default = datetime.now() + timedelta(days=90), readonly=True, copy=False)
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string='Garden Orientation')
    active = fields.Boolean('Active', default=True)
    state = fields.Selection([
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled')
    ], default='new', required=True)
