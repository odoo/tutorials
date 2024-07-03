from odoo import models, fields


class Estate(models.Model):
    _name = "estate.property"
    _description = "Estate Property Plans"

    name = fields.Char("Property Name", required=True)
    description = fields.Text("Property Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Date Availibility")
    expected_price = fields.Float("Expected Price", required=True)
    sellig_price = fields.Float("Selling Price", required=True)
    bedrooms = fields.Integer("Bedrooms")
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
