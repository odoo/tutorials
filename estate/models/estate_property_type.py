from odoo import fields, models


class PropertyType(models.Model):
    # Attributes
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    # Fields
    name = fields.Char(string="Name", required=True)

    # SQL Constraints
    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "The property type name must be unique.",
    )
