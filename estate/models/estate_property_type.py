from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    _sql_constraints = [
        ("check_unique_name", "UNIQUE(name)",
        "A property tag name must be unique")
    ]

    name = fields.Char(required=True)
