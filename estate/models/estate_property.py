from odoo import models, fields

class Property(models.Model):
    _name = "estate_property"
    _description = "estate property model"

    name = fields.Char('Nom', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Post Code')
    date_availability = fields.Date('Date Availability')
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Prince')
    bedrooms = fields.Integer('# Bedrooms')
    living_area = fields.Integer('# Living Areas')
    facades = fields.Integer('# Facades')
    garage = fields.Boolean('Has Garage')
    garden = fields.Boolean('Has Garden')
    garden_area = fields.Integer('# Garden Areas')
    garden_orientation = fields.Selection(
        string = 'Garden Orientation',
        selection=[('north', 'North'), ('south','South'),('east','East'),('west','West')]
    )



