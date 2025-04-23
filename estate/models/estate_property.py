from dateutil import relativedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char(string="Name of the Property", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Date of Availability",
        copy=False,
        default=fields.Date.today() + relativedelta.relativedelta(months=3),
    )
    expected_price = fields.Float(
        string="Expected Selling Price",
        required=True,
    )
    selling_price = fields.Float(
        string="Selling Price",
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    living_area = fields.Integer(string="Number of Living Areas")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Has a garage")
    garden = fields.Boolean(string="Has a garden")
    garden_area = fields.Integer(string="Number of garden Areas")
    garden_orientation = fields.Selection(
        string="Orientation of the Garden",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )

    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )
    users_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer")
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )
