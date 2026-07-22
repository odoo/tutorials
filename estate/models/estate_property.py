from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "realestate.estate.properties"
    _description = "Real estate properties"

    active = fields.Boolean(default=False)
    name = fields.Char("Plan Name", required=True, translate=True)
    description = fields.Text("Notes")
    postcode = fields.Char("Postcode", required=True)
    date_availability = fields.Date(
        "Availability date",
        copy=False,
        default=date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float("Expected price", required=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        default="new",
        copy=False,
    )
    selling_price = fields.Float("Selling price", copy=False, readonly=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living area")
    facades = fields.Integer("Facades")
    garages = fields.Boolean("Garages")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden area")
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
