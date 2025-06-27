from odoo import fields, models


class EstatePropertyTag(models.Model):
    """Model representing a property tag."""

    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'The tag name must be unique.'),
    ]

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")
