import random
from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "A real estate property"

    def _three_month_from_now(self):
        """Return as ORM date compliant value three month from today"""

        return fields.Date.today(self) + relativedelta(months=3)

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Estate Description")
    active = fields.Boolean(default=True)

    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        string="State",
        required=True,
        copy=False,
    )

    postcode = fields.Char()

    date_availability = fields.Date(string="Available From", copy=False, default=_three_month_from_now)

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=random.randint(2, 6))
    facades = fields.Integer()
    living_area = fields.Integer()
    garden_area = fields.Integer()

    garage = fields.Boolean()
    garden = fields.Boolean()

    garden_orientation = fields.Selection(
        string="Type",
        selection=[
            ("north", "North"),
            ("east", "East"),
            ("south", "South"),
            ("west", "West"),
        ],
    )

    # Related fields

    property_type_id = fields.Many2one("estate.property.type", string="Type")
    property_type_test_value = fields.Char(
        string="Test Value",
        related="property_type_id.test_value",
        readonly=True,
    )

    property_tag_ids = fields.Many2many("estate.property.tag", string="Tag")

    property_offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Offers",
    )

    # Related fields RES

    partner_id = fields.Many2one("res.partner", string="Partner", copy=False)
    user_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
