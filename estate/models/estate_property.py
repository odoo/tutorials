from odoo import fields, models, api
from datetime import timedelta


class EstateProperty(models.Model):

    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        default=lambda self: fields.Date.today() + timedelta(days=90),
        copy=False,
    )
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(
        string="Selling Price",
        copy=False,
        readonly=True,
    )
    bedrooms = fields.Integer(
        string="Bedrooms",
        default=2,
    )
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garden = fields.Boolean(string="Garden")
    garage = fields.Boolean(string="Garage")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        required=True,
        default="new",
        copy=False,
    )
    property_type_id = fields.Many2one(
    "estate.property.type",
    string="Property Type"
    )
   
    