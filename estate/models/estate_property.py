from datetime import datetime

from dateutil.relativedelta import relativedelta
from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")

    def _default_Date(self):
        return datetime.now() + relativedelta(months=3)

    property_type_id = fields.Many2one("estate.property.type", "Type")
    date_availability = fields.Date("Available From", copy=False, default=_default_Date)
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float(
        "Selling Price",
        readonly=True,
        copy=False,
    )
    sales_man_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    property_tag_ids = fields.Many2many("estate.property.tag", "Tags")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    active = fields.Boolean(string="Active", default=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    state = fields.Selection(
        [
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
