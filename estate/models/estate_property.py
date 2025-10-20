from odoo import fields, models

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char('Property Name', required=True)
    description = fields.Text('Property Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Datetime('Date Availability')
    expected_price = fields.Float('Expected Price')
    selling_price = fields.Float('Selling Price', required=True)
    bedrooms = fields.Integer('Bedrooms')
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')],
        help="Type is used to separate Leads and Opportunities")