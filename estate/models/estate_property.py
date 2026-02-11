from dateutil.relativedelta import relativedelta
from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property model"

    name = fields.Char("Title", required=True)
    description = fields.Text("Description", help="write the desc of this prop")
    postcode = fields.Char("Postcode", help="address postal code")
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
    active = fields.Boolean("active", default=True)
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
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    property_tag_ids = fields.Many2many(
        "estate.property.tag", "estate_propery_tags_relation", string="Tags"
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
