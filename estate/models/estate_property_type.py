from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    # SQL Constraints
    # Property type name must be unique
    _unique_property_type = models.Constraint(
        'UNIQUE(name)',
        'The property type must be unique',
    )

    name = fields.Char(required=True)
