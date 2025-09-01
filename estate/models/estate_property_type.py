
from odoo import fields, models


# estate.property.type model
class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type database table"

    name = fields.Char(required=True)
    _sql_constraints = [
        (
            "unique_property_type",
            "unique(name)",
            "Property type should be unique",
        ),
    ]
