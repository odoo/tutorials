from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tag"

    name = fields.Char(string="property tag", required=True)

    _check_name_unique = models.Constraint(
        "unique(name)",
        "The Property Tag must be unique.",
    )
