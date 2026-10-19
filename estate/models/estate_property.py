from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    name = fields.Char("Estate Name", required=True, translate=True)
    description = fields.Text("Description")
    postcode = fields.Char("PostCode")
    date_availability = fields.Date(
        "Availability date",
        copy=False,
        default=fields.Datetime.today() + relativedelta(months=3),
    )

    expected_price = fields.Float("Expected price")
    selling_price = fields.Float("Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        [("n", "North"), ("s", "South"), ("w", "West"), ("e", "East")]
    )

    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        [
            ("n", "New"),
            ("r", "Offer received"),
            ("a", "Offer accepted"),
            ("s", "Sold"),
            ("c", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="n",
    )
