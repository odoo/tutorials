from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tags"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer("Color", default=0)

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "This name is already taken",
    )
