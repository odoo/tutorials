from typing_extensions import Required

from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate property"

    name = fields.Char("Property Name", required = True)
    description = fields.Text("Description")
    postcode = fields.Char("Zip Code")
    date_availability = fields.Date("Availability Date")
    expected_price = fields.Float("Expected Price", required = True)
    selling_price = fields.Float("Selling Price")
    bedrooms = fields.Integer("Number of Bedrooms")
    living_area = fields.Integer("Number of distinct Living Areas")
    facades = fields.Integer("Number of Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(string="Garden Orientation", selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')])
