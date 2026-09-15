from odoo import fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char("Property Name", required=True)
    descritpion = fields.Text("Property Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available Date")
    expected_price = fields.Float("Expected Price")
    selling_price = fields.Float("Selling Price", required=True)
    bedrooms = fields.Integer("Number of Bedrooms")
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Number of Facades")
    has_garage = fields.Boolean("Has a Garage")
    has_garden = fields.Boolean("Has a Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
            selection=[
                ("north", "North"),
                ("south", "South"), 
                ("east", "East"), 
                ("west", "West")
            ]
    )
