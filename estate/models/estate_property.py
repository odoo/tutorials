# The aim is to create a table...
from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "This is estate model"
    name = fields.Char(string = "Name", required = True)
    create_uid = fields.Integer(string = "Creation ID")
    write_uid = fields.Integer(string = "Write ID")
    description = fields.Text(string = "Description", required = True)
    postcode = fields.Char(string = "Postcode")
    date_availability = fields.Date(string = "Date Availability")
    expected_price = fields.Float(string = "Expected Price")
    selling_price = fields.Float(string = "Selling Price")
    bedrooms = fields.Integer(string = "Bedrooms")
    living_area = fields.Integer(string = "Living Area")
    facades = fields.Integer(string = "Facades")
    garage = fields.Boolean(string = "Garage")
    garden = fields.Boolean(string = "Garden")
    garden_area = fields.Integer(string = "Garden Area")
    garden_orientation = fields.Selection(
        string = "Garden Orientation",
        selection = [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )

    