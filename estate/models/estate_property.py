from odoo import fields, models


class estate_property(models.Model):

    _name = "estate.property"
    _description = "The estate property"
    name = fields.Char("Property name", required=True)
    description = fields.Text()
    postcode = fields.Char()
    active = fields.Boolean(default=True)
    date_availability = fields.Date(
        default=fields.Date.add(fields.Date.today(), months=3)
    )

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Type",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("west", "West"),
            ("east", "East"),
        ],
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="State",
        required=True,
        copy=False,
        default="new",
    )
