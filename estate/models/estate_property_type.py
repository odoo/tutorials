from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Test description for estate.property.type model"

    name               = fields.Char(required=True)

    _check_name = models.Constraint(
        "UNIQUE (name)",
        "Property type name must be unique"
    )