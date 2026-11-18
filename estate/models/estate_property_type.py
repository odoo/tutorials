from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Type Description"

    name = fields.Char(required=True)

    _name_unique = models.Constraint(
        "UNIQUE(name)",
        "The name must be unique.",
    )
