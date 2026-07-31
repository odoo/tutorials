from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(required=True)
    _check_property_type_name = models.Constraint(
        "UNIQUE(name)",
        "A property type name must be unique",
    )
