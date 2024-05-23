from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property"
    _order = "sequence"
    name = fields.Char('Property Name', required=True)
    description = fields.Text('Description', required=False)
    postcode = fields.Char('Postcode', required=False)
    date_availability = fields.Date('Available From')
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('Bedrooms', default=0)
    living_area = fields.Integer('Living Area (sqm)', default=1)
    facades = fields.Integer('Facades', default=0)
    garage = fields.Boolean('garage', default=False)
    garden = fields.Boolean('garden', default=False)
    garden_area = fields.Integer('garden Area (sqm)', default=0)
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="orientation of the garden relative to the porperty")