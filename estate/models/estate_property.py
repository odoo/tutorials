from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Storing Properties of Real Estate"

    name = fields.Char(string="property_name", required=True)
    description = fields.Text(string="property_description")
    postcode = fields.Char("property_postcode")
    date_availability = fields.Date(
        string="property_date_availability",
        default=fields.Date.add(fields.Date.today(), months=3),
        copy=False,
    )
    expected_price = fields.Float(string="property_expected_price", required=True)
    selling_price = fields.Float(
        string="property_selling_price", readonly=True, copy=False
    )
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [("North", "north"), ("South", "south"), ("East", "east"), ("West", "west")]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("New", "new"),
            ("Offer Received", "Offer Received"),
            ("Offer Accepted", "Offer Accepted"),
            ("Sold", "sold"),
            ("Cancelled", "cancelled"),
        ],
        default="New",
        copy=False,
    )
