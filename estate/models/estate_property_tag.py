from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    # Constraints
    _uniq_name = models.Constraint(
        "UNIQUE(name)",
        "A property tag's name must be unique.",
    )
