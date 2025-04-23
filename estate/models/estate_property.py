from dateutil import relativedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate property"

    name = fields.Char("Title", required=True)
    active = fields.Boolean("Active", default=True)
    description = fields.Text()
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Available From",
        copy=False,
        default=fields.Date.today() + relativedelta.relativedelta(months=3),
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
        copy=False,
    )
    property_type_id = fields.Many2one("estate_property_type", "Property Type")
    salesman_id = fields.Many2one(
        "res.users",
        "Salesman",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one("res.partner", "Buyer", copy=False)
    tag_ids = fields.Many2many("estate_property_tag", string="Tags")
    offer_ids = fields.One2many(
        "estate_property_offer",
        "property_id",
    )
