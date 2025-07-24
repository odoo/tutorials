from odoo import fields, models


class NinjaTurtlesEstatePropertyType(models.Model):
    _name = "ninja.turtles.estate.property.type"
    _description = "Ninja Turtle Estate for faster Property Type"

    name = fields.Char(required=True)
