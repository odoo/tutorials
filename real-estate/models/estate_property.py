from odoo import fields, models
from dateutil.relativedelta import relativedelta 

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Properties involved in estate"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Availability Date",
        copy=False,
        default=fields.Date.add(fields.Date.today() , months = 3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )

    # reserved fields
    active = fields.Boolean(default=False)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_recieved", "Offer Recieved"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Invoice Status",
        default="new",
        required=True,
        copy=False,
    )
