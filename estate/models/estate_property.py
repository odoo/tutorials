from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"

    name = fields.Char(required=True, string="Title")
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    available_from = fields.Date(
        string="Available From",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(default=2, string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        default="north",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canclled", "Cancelled"),
        ],
        default="new",
    )
