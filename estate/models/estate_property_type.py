from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"

    name = fields.Char(required=True)


    _sql_constraints = [
        (
            "unique_property_type",
            "UNIQUE(name)",
            "A tag with same property type already exist",
        ),
    ]
