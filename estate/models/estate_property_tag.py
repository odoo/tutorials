from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    _sql_constraints = [
        ("check_unique_name", "UNIQUE(name)",
        "A property tag name must be unique")
    ]

    name = fields.Char(required=True)
