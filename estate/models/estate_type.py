from odoo import fields, models


class EstateType(models.Model):
    _name = "estate.type"
    _description = "An estate type"

    name = fields.Char(required=True)

    # Constraints
    _check_name = models.Constraint(
        "UNIQUE(name)",
        "A type must be unique",
    )
