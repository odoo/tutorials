from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()
    _check_unique_name = models.Constraint(
        "UNIQUE(name)",
        "The name must be unique",
    )
