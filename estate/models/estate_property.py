from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description", required=True)
    postcode = fields.Char(
        string="Postcode",
    )
    date_availability = fields.Date(
        string="Date of Availability",
    )
    expected_price = fields.Float(
        string="Expected Price",
        required=True,
    )
    selling_price = fields.Float(
        string="Selling Price",
    )
    bedrooms = fields.Integer(
        string="Bedrooms",
    )
    living_area = fields.Integer(
        string="Living Area (sqm)",
    )
    facades = fields.Integer(
        string="Number of Facades",
    )
    garage = fields.Boolean(
        string="Has Garage",
    )
    garden = fields.Boolean(
        string="Has Garden",
    )
    garden_area = fields.Integer(
        string="Garden Area (sqm)",
    )
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
