from dateutil import relativedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate: Property"

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    active = fields.Boolean("Active", default=True)

    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Availability Date",
        copy=False,
        default=fields.Date.today() + relativedelta.relativedelta(months=3),
    )

    expected_price = fields.Float("Expected Price", required=True, default=0.0)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)

    bedrooms = fields.Integer("# of bedrooms", default=2)
    living_area = fields.Integer("# of living areas")
    facades = fields.Integer("# of facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
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
        required=True,
        copy=False,
        default="new",
    )
