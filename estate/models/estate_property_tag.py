from odoo import fields, models


class PropertyTag(models.Model):
    # Attributes
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    # Fields
    name = fields.Char(required=True)

    # SQL Constraints
    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "The property tag name must be unique.",
    )
