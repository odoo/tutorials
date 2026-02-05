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
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
        copy=False,
    )
    expected_price = fields.Float(
        string="Expected Price",
        required=True,
    )
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
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
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="new",
        copy=False,
    )
    active = fields.Boolean(string="Active", default=False)
    