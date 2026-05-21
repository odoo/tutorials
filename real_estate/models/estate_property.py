from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "real estate property module"

    name = fields.Char(string="Property Name")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postal Code")
    date_availability = fields.Date(
        string="Available From", default=lambda self: fields.Date.today()
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", required=True)
    bedrooms = fields.Integer(string="Bedroom Count")
    living_area = fields.Integer(string="Living Area Count")
    facades = fields.Integer(string="Facades Count")
    has_garage = fields.Boolean(string="Has any Garage ?")
    has_garden = fields.Boolean(string="Has any Garden ?")
    garden_area = fields.Integer(string="Garden Area in (sq meter)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(string="Field Activity Status", default=True)
    state = fields.Selection(
        string="Property State",
        selection=[
            ("1", "New"),
            ("2", "Offer Received"),
            ("3", "Offer Accepted"),
            ("4", "Sold"),
            ("5", "Cancelled"),
        ],
        default="1",
    )
