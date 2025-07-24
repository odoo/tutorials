from odoo import models, fields


class NinjaTurtlesEstatePropertyTag(models.Model):
    _name = "ninja.turtles.estate.property.tag"
    _description = "Ninja Turtle Estate for faster Property Tag"

    name = fields.Char(required=True)
