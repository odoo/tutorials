from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property definition"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.context_today(self) + relativedelta(months=3),
        copy=False,
    )
    expected_salary = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(
        default=2,
    )
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(required=True)
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )

    state = fields.Selection(
        selection=[
            ("New", "New"),
            ("Offer Accepted", "Offer Accepted"),
            ("Offer Received", "Offer Received"),
            ("Sold", "Sold"),
            ("Cancelled", "Cancelled"),
        ],
        string="State",
    )

    active = fields.Boolean(default=False)
