from odoo import fields, models


class EstateProperty(models.Model):
    _name = "realestate.estate.properties"
    _description = "Real estate properties"

    name = fields.Char('Plan Name', required=True, translate=True)
    description = fields.Text('Notes')
    postcode = fields.Char('Postcode', required=True)
    date_availability = fields.Date('Availability date')
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price')
    bedrooms = fields.Integer('Bedrooms')
    living_area = fields.Integer('Living area')
    facades = fields.Integer('Facades')
    garages = fields.Boolean('Garages')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
