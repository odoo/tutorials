from odoo import fields, models

class TestModel(models.Model):

    _name = "estate.property"
    _description = "Declare property for Real estate"

    # --------------------------------------- Fields Declaration ----------------------------------

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From")
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price")
    bedrooms = fields.Integer("Bedrooms")
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    is_garage = fields.Boolean("Garage")
    is_garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (yard)")
    garden_orientation = fields.Selection(
        string="Garden Oientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Type is used to separate garden orientation uses",
    )
