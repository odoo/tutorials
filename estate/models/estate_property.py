from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    def _default_date_availability(self):
        return fields.Date.today() + relativedelta(months=3)

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()

    date_availability = fields.Date(
        copy=False,
        default=_default_date_availability,
        # default=lambda self: fields.Date.today() + relativedelta(months=3)
    )

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False, default=3000)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [("North", "North"), ("South", "South"), ("East", "East"), ("West", "West")]
    )
    state = fields.Selection(
        [
            ("New", "New"),
            ("Offer Recieved", "Offer Received"),
            ("Offer Accepted", "Offer Accepted"),
            ("Sold", "Sold"),
            ("Cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="New",
    )
    active = fields.Boolean(default=False)
