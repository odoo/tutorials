from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate Property"

    name = fields.Char(string="Property Name", required=True)
    description = fields.Char(string="Property Description")
    postcode = fields.Char(string="Postal Code")
    date_availability = fields.Date(string="Available From")
    expected_price = fields.Float(string="Expected Selling Price", required=True)
    selling_price = fields.Float(string="Actual Selling Price")
    bedrooms = fields.Integer(string="Number of Bedrooms")
    living_area = fields.Float(string="Living Area (sqm)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Float(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
