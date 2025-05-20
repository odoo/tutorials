from odoo import fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Property's properties"

    name = fields.Char('Property name', required=True)
    description = fields.Text('Property description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability')
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price')
    bedrooms = fields.Integer('Bedrooms')
    living_area = fields.Integer('Living area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection([('North', 'North'), ('East', 'East'), ('South', 'South'), ('West', 'West')], default='North')
