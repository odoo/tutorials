from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availabilty Date')
    expected_price = fields.Float(required=True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('Bedrooms')
    living_area = fields.Integer('Livingf Area')
    facades = fields.Integer()
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
