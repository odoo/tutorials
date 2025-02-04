from odoo import fields, models

class EstateProperty(models.Model):
    _name = "real_estate_property"
    _description = "Real Estate Property Plans"

    name = fields.Char(string='Property Name', required=True)

    description = fields.Text(string='Description')

    postcode = fields.Char(string='Postcode')

    date_availability = fields.Date(string='Availability Date')

    expected_price = fields.Float(string='Expected Price', required=True)

    selling_price = fields.Float(string='Selling Price')

    bedrooms = fields.Integer(string='Bedrooms')

    living_area = fields.Integer(string='Living Area')

    facades = fields.Integer(string='Facades')

    garage = fields.Boolean(string='Garage')

    garden = fields.Boolean(string='Garden')

    garden_area = fields.Integer(string='Garden Area')
    
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string='Garden Orientation')
    
