from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    _check_unique_name = models.Constraint(
        "UNIQUE (name)",
        "The name must be unique",
    )

    name = fields.Char(required=True)
