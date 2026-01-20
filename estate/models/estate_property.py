from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate_property'
    _description = 'Estate Property'

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Post Code')
    date_availability = fields.Date('Availability Date')
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('# Bedrooms')
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('# Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'), ('south', 'South'),
            ('east', 'East'), ('west', 'West')
        ])
