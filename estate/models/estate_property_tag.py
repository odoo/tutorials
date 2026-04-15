from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real E-state Property Tag"

    name = fields.Char(required=True)

    _check_unique_tag = models.Constraint(
        "UNIQUE(name)",
        "A property tag name must be unique",
    )
