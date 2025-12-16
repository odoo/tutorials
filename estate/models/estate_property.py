from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate property"

    name = fields.Char('Property Name', required=True)
    description = fields.Text('Property Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability Date')
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('# Bedrooms')
    living_area = fields.Integer('# Living Area')
    facades = fields.Integer('# Facades')
    garage = fields.Boolean('Has Garage')
    garden = fields.Boolean('Has Garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(
        string='type',
        selection=[
        ('North', 'North Garden Orientation'),
        ('South', 'South Garden Orientation'),
        ('East', 'East Garden Orientation'),
        ('West', 'West Garden Orientation')
    ])
    
