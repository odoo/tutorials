from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char("Property Name", required=True)
    description = fields.Text("Property Description")
    postcode = fields.Char("Postcode")

    date_availability = fields.Date("Available Date", copy=False, default=lambda _x: datetime.now() + relativedelta(months=+3))

    expected_price = fields.Float("Expected Price")
    selling_price = fields.Float("Selling Price", copy=False, readonly=True)

    bedrooms = fields.Integer("Number of Bedrooms", default=2)
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
            ("west", "West"),
        ],
    )

    state = fields.Selection(
        string="Property State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )

    active = fields.Boolean(default=True)
