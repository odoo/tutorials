from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "An estate property tag"
    _order = "name, id"

    name = fields.Char(required=True)
    color = fields.Integer()

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "A property tag name must be unique.",
    )
