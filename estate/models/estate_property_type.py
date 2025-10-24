from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)

    _unique_property_type_name = models.Constraint(
        "UNIQUE(name)",
        "The tag name must be unique.",
    )
