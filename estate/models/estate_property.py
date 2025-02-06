from odoo import fields, models
from dateutil.relativedelta import relativedelta

class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(
        "Title", required=True,
        help="This field specifies the estate property name.",
    )
    description = fields.Text(
        "Description",
        help="This field specifies the description of property in brief to provide insights on the property.",
    )
    postcode = fields.Char(
        "Postcode", help="This field specifies the postcode of the property address."
    )
    date_availability = fields.Date(
        "Available From", readonly=False, default=fields.Date.today() + relativedelta(months=3),
        help="This field specifies the date when the property will be available.",
    )
    expected_price = fields.Float(
        "Expected Price", required=True,
        help="This field specifies the price expected for the property.",
    )
    selling_price = fields.Float(
        "Selling Price", readonly=True, copy=False,
        help="This field specifies the actual selling price of the property.",
    )
    bedrooms = fields.Integer(
        "Bedrooms", default=2,
        help="This field specifies the number of bedroom that this property consists of.",
    )
    living_area = fields.Integer(
        "Living Area (sqm)",
        help="This field specifies the size of living area (in sqm.) of the property.",
    )
    facades = fields.Integer(
        "Facades",
        help="This field specifies the facade i.e. the exterior or the front of a property.",
    )
    garage = fields.Boolean(
        "Garage",
        help="This field specifies if the property has a garage",
    )
    garden = fields.Boolean(
        "Garden",
        help="This field specifies if the property has a garden",
    )
    garden_area = fields.Integer(
        "Garden Area (sqm)",
        help="This field specifies the size of garden area (in sqm.) of the property.",
    )
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="This selection fields specifies the facing direction of garden (North, South, East, or West).",
    )
    state = fields.Selection(
        string="Property Status", copy=False, required=True, default="new",
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
        ],
        help="This selection fields specifies the state of the property.",
    )
    active = fields.Boolean(
        "Active", default=True,
        help="This specifies if the property should be listed."
    )
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type",
        help="This specifies the type of the property."
    )
    buyer = fields.Many2one(
        "res.partner", string="Buyer", copy=False,
        help="Buyer of the property."
    )
    salesperson = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user,
        help="Sales Person associated with the property."
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Property Offers")
