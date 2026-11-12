
from odoo import fields, models

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price')
    living_area = fields.Integer(string='Living Area')
    postcode = fields.Char(string='Postcode')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    date_availability = fields.Date(string='Availability Date')
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    bedrooms = fields.Integer(string='Bedrooms')


