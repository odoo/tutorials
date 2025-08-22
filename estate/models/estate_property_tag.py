from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Adds different property tags"
    _sql_constraints = [
        (
            "property_tag_unique",
            "UNIQUE (name)",
            "Property Tag already exists.",
        ),
    ]
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()
