from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Adds different property types"
    _sql_constraints = [
        (
            "property_type_unique",
            "UNIQUE (name)",
            "Property Type already exists.",
        ),
    ]

    name = fields.Char(required=True)
