from odoo import fields, models


class EstatePropertyTypes(models.Model):
    _name = "estate.property.type"
    _description = "Real E-state Property Type"

    name = fields.Char()

    _check_unique_property_name = models.Constraint(
        "UNIQUE(name)",
        "A property type should be unique",
    )
