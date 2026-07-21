from odoo import api, models, fields
from dateutil.relativedelta import relativedelta


@api.model
def _default_date_availability(self):
    return fields.Date.today() + relativedelta(months=3)


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    active = fields.Boolean(default=True)

    name = fields.Char(required=True, default="Unknown")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=_default_date_availability)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
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
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        required=True,
        copy=False,
        default="new",
    )
