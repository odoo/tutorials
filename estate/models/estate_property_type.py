from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _check_unique_name = models.Constraint(
        "UNIQUE (name)",
        "The name must be unique",
    )

    name = fields.Char(required=True)
