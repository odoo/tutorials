from odoo import fields, models


class EstateTag(models.Model):
    _name = "estate.tag"
    _description = "An estate tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    # Constraints
    _check_name = models.Constraint(
        "UNIQUE(name)",
        "A tag name must be unique",
    )
