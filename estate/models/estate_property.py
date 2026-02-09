from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property definition"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    data_availability = fields.Date()
    expected_salary = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(required=True)
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
