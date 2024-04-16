from odoo import models,fields

class Property(models.Model):
    """Class representing the properties of the estate module"""

    _name = "estate_property"
    _description = "The properties of the real estate module"
    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required = True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection = [('North', 'North'), ('SOUTH', 'SOUTH'), ('EAST', 'EAST'), ('WEST', 'WEST')])
