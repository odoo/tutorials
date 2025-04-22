from typing import Required
from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Real Estate: Property"

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availablility = fields.Date("Availibility Date")
    exprected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price")
    bedrooms = fields.Integer("# of bedrooms")
    living_area = fields.Integer("# of living areas")
    facades = fields.Integer("# of facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        selection = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )