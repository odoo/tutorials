from odoo import fields, models


class NinjaTurtlesEstatePropertyType(models.Model):
    _name = "ninja.turtles.estate.property.type"
    _description = "Ninja Turtle Estate for faster Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Property type name must be unique.')
    ]

    property_ids = fields.One2many("ninja.turtles.estate",
                                   "property_type_id",
                                   string="Properties")

    sequence = fields.Integer('Sequence', default=1)
