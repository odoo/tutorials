from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Test description for estate.property.tag model"

    _order = "name"

    name = fields.Char(required=True)

    _check_name = models.Constraint(
        "UNIQUE (name)",
        "Property tag name must be unique",
    )

    color = fields.Integer()
