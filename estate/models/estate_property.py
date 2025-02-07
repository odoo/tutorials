from odoo import fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    def _default_date_availability(self):
        return datetime.today() + relativedelta(months=3)

    active = fields.Boolean(default=True)
    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postal Code")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Garage Available")
    garden = fields.Boolean(string="Garden Available")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    state = fields.Selection(
        string="Status of Document",
        selection=[
            ("new", "New"),
            ("offer Received", "Offer Received"),
            ("offer Accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )
    date_availability = fields.Date(
        string="Available From", copy=False, default=_default_date_availability
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    partner_id = fields.Many2one("res.partner", string="Buyer", copy="False")
    users_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id")
