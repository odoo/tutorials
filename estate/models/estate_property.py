from odoo import models, fields
from datetime import date,timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True, string="Title")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        default=date.today() + timedelta(days=90),
        copy=False
        )
    expected_price = fields.Float(required=True, string="Expected Price")
    postcode = fields.Integer(required=True, string="Postcode")
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Has Garage?")
    garden = fields.Boolean(string="Has Garden?")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
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
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type"
    )
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user       
    )
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer", copy=False
    )
    tags_ids = fields.Many2many(
        "estate.property.tag", string=" PropertyTags"
    )
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id",string="Offers"
    )