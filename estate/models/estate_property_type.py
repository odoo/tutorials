from odoo import fields, models


class EstateTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type Model"

    name = fields.Char(required=True)

    _sql_constraints = [
        (
            "check_property_type_name",
            "UNIQUE(name)",
            "Property Type Name must be unique",
        )
    ]
