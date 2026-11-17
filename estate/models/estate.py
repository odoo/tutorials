from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "A Free Real Estate Property"

    name = fields.Char('Name', required=True, translate=True)
    description = fields.Text('Name', required=False, translate=True)
    postcode = fields.Char('Postcode', required=False, translate=True)
    date_availability = fields.Date('Availability', required=False, translate=True)
    expected_price = fields.Float('Expected price', required=True, translate=True)
    selling_price = fields.Float('Selling price', required=False, translate=True)
    bedrooms = fields.Integer('Bedrooms', required=False, translate=True)
    living_area = fields.Integer('Living areas', required=False, translate=True)
    facades = fields.Integer('Facades', required=False, translate=True)
    garage = fields.Boolean('Garage', required=False, translate=True)
    garden = fields.Boolean('Garden', required=False, translate=True)
    garden_area = fields.Integer('Integer', required=False, translate=True)
    garden_orientation = fields.Selection(string='Garden orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Determines garden's orientation")