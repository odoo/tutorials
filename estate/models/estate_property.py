from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate properties"

    name = fields.Char("Title", required=True)
    description = fields.Text("description")
    postcode = fields.Integer("Postcode")
    date_availability = fields.Date("Available from")
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price")
    bedrooms = fields.Integer("Bedrooms")
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
