from odoo import fields, models

class RealEstate(models.Model):
    _name = "real.estate.property"
    _description = 'Real State propperties'
    _order = 'sequence'

    name = fields.Char(string = 'Name', required = True)
    description = fields.Text(string = 'Description')
    postcode = fields.Char(string = 'Post Code')
    date_availability = fields.Date(string = 'Date Availability')
    expected_price = fields.Float(string = 'Expected Price', required = True)
    bedrooms = fields.Integer(string = 'Bedrooms')
    living_area = fields.Integer(string = 'Living Area')
    facades = fields.Integer(string = 'Facades')
    garage = fields.Boolean(string = 'Garage')
    garden = fields.Boolean(string = 'Garden')
    garden_area = fields.Integer(string = 'Garden Area')
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')

        ],
        string = 'Garden Orientation'

    )



    