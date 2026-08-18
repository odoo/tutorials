from odoo import fields, models


class EstateTag(models.Model):
    _name = "estate.tag"
    _description = "An estate tag"

    name = fields.Char(required=True)

    # Constraints
    _check_name = models.Constraint(
        "UNIQUE(name)",
        "A tag name must be unique",
    )
