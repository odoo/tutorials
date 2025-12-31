from odoo import models, fields


class real_estate(models.Model):
    _name = 'real.estate'
    _description = 'Real Estate Property'

    name = fields.Char(string='Name', default="Unknown", required=True)
    street_address = fields.Char(string='Street Address')
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Datetime(string='Date Availability', default=fields.Datetime.now)
    expected_price = fields.Float(string='Expected Price')
    selling_price = fields.Float(string='Selling Price', default=1000)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area')
    bathrooms = fields.Integer(string='Bathrooms')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
