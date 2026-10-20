from odoo import fields, models


class PropertyTypes(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Types"

    name = fields.Char(string="Property Type", required=True)

    _check_name = models.Constraint(
        "unique (name)",
        "A property type name must be unique.",
    )
