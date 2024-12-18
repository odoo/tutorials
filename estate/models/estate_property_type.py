
from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "The type of a property"

    _sql_constraints = [
        (
            "name",
            "unique(name)",
            "The name of the property type must be unique.",
        )
    ]

    name = fields.Char(required=True)
