from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "It stores the property types"

    name = fields.Char(required=True)

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "The property type name must be unique.",
    )
