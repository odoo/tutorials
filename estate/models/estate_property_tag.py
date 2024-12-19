from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag for estate properties"
    _order = "name"

    _sql_constraints = [
        (
            "name",
            "unique(name)",
            "The name of the property tag must be unique.",
        )
    ]

    name = fields.Char(required=True)
    color = fields.Integer()
