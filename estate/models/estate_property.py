from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "sequence"

    name = fields.Char('Property Name', required=True, translate=True)
    barn = fields.Char(string='Namei barn', required=True, translate=True)

    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date of Availability')
    expected_price = fields.Float('Expected Price')
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('Number of Bedrooms')
    living_area = fields.Integer('Living Area (in sq.m.)')
    facades = fields.Integer('Number of Facades')
    garage = fields.Boolean('Has Garage')
    garden = fields.Boolean('Has Garden')
    garden_area = fields.Integer('Garden Area (in sq.m.)')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string="Garden Orientation")

    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence', default=10)

    # _sql_constraints = [
    #     ('check_number_of_months', 'CHECK(number_of_months >= 0)', 'The number of months can\'t be negative.'),
    # ]
