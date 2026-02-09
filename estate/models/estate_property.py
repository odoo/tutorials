from odoo import models, fields
from dateutil.relativedelta import relativedelta


class RealEstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property model"

    name = fields.Char("Title", required=True)
    description = fields.Text("Description", help="write the desc of this prop")
    postcode = fields.Char("Post Code", help="address postal code")
    date_availability = fields.Date(
        "Available From",
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float("Expected Price", default=0.00, required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2, help="Number of Bedrooms")
    living_area = fields.Integer("Living Area(sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage", default=False)
    garden = fields.Boolean("Garden", default=False)
    garden_area = fields.Integer("Garden Area(sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean("active", default=False)
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        default="new",
        copy=False,
    )
