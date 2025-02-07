from odoo import models, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "public.property"
    _description = "Estate related data"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Available From",
        default=lambda self: (datetime.today() - relativedelta(month=3)).date(),
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("east", "East"),
            ("west", "West"),
            ("south", "South"),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            (
                "offer_received",
                "Offer Received",
            ),
            (
                "offer_accepted",
                "Offer Accepted",
            ),
            (
                "sold_and_cancelled",
                "Sold and Cancelled",
            ),
        ],
        default="new",
        required=True,
        copy=False,
    )
