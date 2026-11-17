from odoo import fields, models


class Property(models.Model):
    _name = "estate_property"
    _description = "Estate property"

    name = fields.Char('Property Name', required=True)
    description = fields.Text('Property Description')
    postcode = fields.Char('')
    date_availability = fields.Date('Availability Date')
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('Bedrooms', help="Number of bedrooms")
    living_area = fields.Integer('Living Area (m²)')
    facades = fields.Integer('Facades', help="Number of facades")
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (m²)')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north','North'),('south','South'),('east','East'),('west','West')],
        help="Indicates the orientation of the garden"
    )