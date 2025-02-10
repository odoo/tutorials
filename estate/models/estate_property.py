from odoo import fields, models
from datetime import datetime, timedelta


class EstateProperty(models.Model):

    _name = "estate.property"
    _description = "Declare property for Real estate"

    # --------------------------------------- Fields Declaration ----------------------------------

    name = fields.Char(required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Available From", default=datetime.now() + timedelta(90)
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", copy=False, readonly=True)
    bedrooms = fields.Integer("Bedrooms", default="2")
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    is_garage = fields.Boolean("Garage")
    is_garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (yard)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Type is used to separate garden orientation uses",
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
        required=True,
        copy=False,
        default="new",
    )
    active = fields.Boolean("Active", default=True)
    # Relational
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
    # Relational Field for tag's (Many2Many)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    # Relation Field for offer (one2Many)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
