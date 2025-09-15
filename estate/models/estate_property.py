from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char("Estate name", required=True, translate=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From")
    expected_price = fields.Float()
    selling_price = fields.Float("Actual Price")
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Orientation of the estate property",
    )
    property_type = fields.Selection(
        selection=[("apartment", "Apartment"), ("house", "House")]
    )
