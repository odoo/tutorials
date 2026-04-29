from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _check_name = models.Constraint(
        "UNIQUE (name)",
        "Each tag name must be unique",
    )
