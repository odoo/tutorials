"""Model of a tag on an estate property."""

from odoo import fields, models


class EstatePropertyTag(models.Model):
    """Estate Property Tag model."""

    _name = "estate.property.tag"
    _description = "Tags for estate properties"
    _sql_constraints = [
        ('name', 'UNIQUE(name)', 'Name must be unique.'),
    ]
    _order = "name"

    name = fields.Char('Name')
    color = fields.Integer('Color', default=1)
