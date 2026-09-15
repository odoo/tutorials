from odoo import fields, models


class Property(models.Model):
    _name = "estate_property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text
    date_availability = fields.Date
    expected_price = fields.Float(required=True)
    selling_price = fields.Float
    bedrooms = fields.Integer
    living_area = fields.Integer
    facades = fields.Integer
    garage = fields.Boolean
    garen = fields.Boolean
    garden_area = fields.Integer
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="The garden orientation",
    )
