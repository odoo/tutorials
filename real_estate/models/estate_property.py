from odoo import fields, models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate Property"

    name = fields.Char(
        string="Property Name", required=True,
        help="Enter the property name."
    )
    description = fields.Text(
        string="Description", help="Brief description of the property."
    )
    postcode = fields.Char(
        string="Postcode", help="Postal code of the property."
    )
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Datetime.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(
        string="Expected Price", required=True,
        help="The price the seller expects."
    )
    selling_price = fields.Float(
        string="Selling Price", readonly=True, copy=False,
        help="The final selling price of the property."
    )
    bedrooms = fields.Integer(
        string="Bedrooms", default=2,
        help="Number of bedrooms in the property."
    )
    living_area = fields.Integer(
        string="Living Area (sq ft)", default=0,
        help="The size of the living area in square feet."
    )
    facades = fields.Integer(
        string="Facades", help="Number of facades the property has."
    )
    garage = fields.Boolean(
        string="Garage", help="Check if the property has a garage."
    )
    garden = fields.Boolean(
        string="Garden", help="Check if the property has a garden."
    )
    garden_area = fields.Integer(
        string="Garden Area (sq ft)",
        compute="_compute_garden_fields", store=True,
        help="Size of the garden in square feet."
    )
    active = fields.Boolean(string="Active", default=True)
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")
        ],
        string="Garden Orientation",
        help="Direction the garden faces."
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        string="State",
        required=True,
        default="new",
        copy=False
    )
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price must be positive."
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Selling price cannot be negative."
        )
    ]
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type",
        help="Type of the Property"
    )
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer", copy=False,
        help="Buyer of the Property"
    )
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson",
        default=lambda self: self.env.user,
        help="Salesperson for the property"
    )
    tag_ids = fields.Many2many(
        "estate.property.tag", string="Property Tags",
        help="Tags for the Property"
    )
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id",
        string="Offers"
    )
