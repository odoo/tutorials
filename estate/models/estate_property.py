from odoo import fields, models
from datetime import timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Module"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")

    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", copy=False, readonly=True)

    expected_date = fields.Date(
        string="Expected Date",
        required=True,
        copy=False,
        default=(fields.Date.today() + timedelta(days=90)),
    )

    bedroom = fields.Integer(string="Number of Bedroom", default=2)
    living_area = fields.Integer(string="Living area (square metter)")
    facades = fields.Integer(string="Number of facades")
    garage = fields.Boolean(string="Have a garage?")
    garden = fields.Boolean(string="Have a garden?")
    garden_area = fields.Integer(string="Garden area (square metter)")
    garden_orientation = fields.Selection(
        string="Garden's orientation",
        selection=[
            ("north", "North"),
            ("sud", "Sud"),
            ("east", " East"),
            ("west", "West"),
        ],
    )
    state = fields.Selection(
        string="Estate's state",
        selection=[
            ("new", "New"),
            ("offer_recieved", "Offer Received"),
            ("offer_accepted", " Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )

    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user
    )

    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)

    property_type_id = fields.Many2one("estate.property.type", string="Type")

    property_tag_ids = fields.Many2many("estate.property.tag", string="Tag")

    proterty_offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    active = fields.Boolean(default=True)
