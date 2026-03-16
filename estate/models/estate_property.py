from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property model"

    name = fields.Char("Name", required=True)
    description = fields.Text("description")

    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=fields.Date.add(fields.Date.today(), days=90),
    )

    expected_price = fields.Float()

    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer("# of bedrooms", default=0)

    living_area = fields.Integer("")
    facades = fields.Integer("# facades")

    garage = fields.Boolean("Has garage")
    garden = fields.Boolean("Has garden")

    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )

    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
    )
