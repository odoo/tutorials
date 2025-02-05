from odoo import fields, models

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char('Property Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postal Code')
    date_availability = fields.Date('Availability Date')
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('Number of bedrooms')
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        selection = [
        ('north','North'),
        ('south','South'),
        ('west','West'),
        ('east','East')]
    )
