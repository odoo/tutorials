from odoo import fields, models
import traceback
from datetime import date
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    traceback.print_stack()
    _name = "estate.property"
    _description = "Real Estate Property"

    def check_availability(self):
        return (date.today() + relativedelta(months=3))

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=check_availability)
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
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        [
            ("New", "New"),
            ("Offer Received", "Offer Received"),
            ("Offer Accepted", "Offer Accepted"),
            ("Sold", "Sold"),
            ("Cancelled", "Cancelled"),
        ],
        default="New",
    )
