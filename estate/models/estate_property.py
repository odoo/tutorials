from odoo import fields, models, api

class EstateModel(models.Model):
    _name = "estate.property"
    _description = "Estate properties"

    name = fields.Char('Title', required=True, translate=True)
    description = fields.Text('Description')
    postcode = fields.Integer('Postcode', help="Your post code in 4 or 5 digits.")
    date_availability = fields.Date('Date Availability')
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer(string='Bedrooms')
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('west', 'West'), ('south', 'South'), ('east', 'East')],
        help="The selection of the garden orientation.")
