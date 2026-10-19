from odoo import fields, models

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Properties'
    _postcode = 'Post default'
    _date_availability = 'availability default'
    _expected_price = 'expected price default'
    _selling_price = 'selling price default'
    _bedrooms = 'bedrooms default'
    _living_area = 'living area default'
    _facades = 'facades default'
    _garage = 'garage default'
    _garden = 'garden default'
    _garden_area = 'garden area default'
    _garden_orientation = 'garden orientation default'

    name = fields.Char('Estate Property', required=True, translate=True)
    description = fields.Char()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Oriented',
        selection=[('north', 'North'), ('south', 'South'),('east', 'East'), ('west', 'West')],
        help="Oriented is used to show which cardinal direction the garden is oriented to")


