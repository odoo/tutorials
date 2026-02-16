from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(string="Property Type", required=True)

    _unique_type_name = models.Constraint(
        "UNIQUE(name)",
        "Property type name must be unique.",
    )
