from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _name_uniq = models.Constraint(
        "UNIQUE (name)",
        "The name of the tag must be unique!",
    )
