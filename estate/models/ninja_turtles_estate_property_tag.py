from odoo import models, fields


class NinjaTurtlesEstatePropertyTag(models.Model):
    _name = "ninja.turtles.estate.property.tag"
    _description = "Ninja Turtle Estate for faster Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'Tag name must be unique.')
    ]

    color = fields.Integer()
