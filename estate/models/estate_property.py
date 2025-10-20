from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Create a new table"

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Post code')
    date_availability = fields.Date(string='Availability date')
    expected_price = fields.Float(string='Expected price', required=True)
    selling_price = fields.Float(string='Selling price')
    bedrooms = fields.Integer(string='Bedrooms')
    living_area = fields.Integer(string='Living area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden area')
    garden_orientation = fields.Selection( 
        string='Garden orientation',
        selection= [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
