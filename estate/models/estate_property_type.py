from odoo import fields, models


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(required=True)

    _sql_constraints = [
        (
            "name",
            "unique(name)",
            "The property type must be unique.",
        )
    ]
