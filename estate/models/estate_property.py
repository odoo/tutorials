import random
from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate_property"
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

    date_availabity = fields.Date(copy=False, default=_three_month_from_now)
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
        selection=[("north", "North"), ("east", "East"), ("south", "South"), ("west", "West")],
    )
