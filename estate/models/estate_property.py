from odoo import fields,models

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Properties of an estate"

    name = fields.Char('Estate Name',required=True, translate=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date Availability')
    expected_price = fields.Float('Expected Price')
    bedrooms = fields.Integer('Bedrooms')
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(string='Type', selection=[('north', 'North'), ('south', 'South'),('west', 'West'), ('east', 'East')])
    