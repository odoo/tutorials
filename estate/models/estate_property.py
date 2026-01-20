from odoo import models, fields

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    name = fields.Char(string='Name', required=True)

    property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('villa', 'Villa'),
    ], string='Property Type')
    postcode = fields.Char(string='Postcode')
    available_from = fields.Date(string='Available From')

    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price')
    best_offer = fields.Float(string='Best Offer')

    description = fields.Text(string='Description')
    bedrooms = fields.Integer(string='Bedrooms', required=True)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string='Garden Orientation')
    total_area = fields.Integer(string='Total Area (sqm)')