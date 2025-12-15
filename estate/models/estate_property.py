from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Advertisement module"

    name = fields.Char('Name', required=True, translate=True)
    description = fields.Text('Description')
    postcode = fields.Char('Poscode', default='1000')
    date_availability = fields.Date('Date availability')
    expected_price = fields.Float('Expected price')
    selling_price = fields.Float('Selling price')
    bedrooms = fields.Integer('Bedrooms')
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection('Gordden orientation', selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])