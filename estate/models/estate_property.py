from odoo import fields, models
from datetime import timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(
        string="Name", required=True, help="Name of the Property"
    )
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Date Availability",
        copy=False,
        default=lambda self: fields.Datetime.today() + timedelta(days=90),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        selection=[
            ("New", "New"),
            ("Offer Received", "Offer Received"),
            ("Offer Accepted", "Offer Accepted"),
            ("Sold", "Sold"),
            ("Cancelled", "Cancelled"),
        ],
        default="New",
        copy=False,
    )
