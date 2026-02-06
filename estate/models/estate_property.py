from datetime import timedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "real estate property"

    name = fields.Char()
    description = fields.Text(required=True)
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.today() + timedelta(days=90),
        copy=False,
    )
    expected_price = fields.Float(readonly=True, copy=False)
    selling_price = fields.Float()
    bedrooms = fields.Integer(default=2)
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
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer receieved"),
            ("offer accepted", "offer accepted"),
            ("sold", "sold"),
            ("cancelled", "cancelled"),
        ],
        default="new",
        required=True,
        copy=False,
    )
