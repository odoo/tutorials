from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"

    _unique_type_name = models.Constraint(
        "UNIQUE(name)",
        "The property type name must be unique.",
    )

    name = fields.Char('Name', required=True)
