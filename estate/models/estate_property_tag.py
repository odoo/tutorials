from odoo import fields, models


class Type(models.Model):
    _name = "estate.property.tag"
    _description = "Tag of property of Estate"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _uniq_name = models.Constraint(
        "unique(name)",
        "A tag name should be unique.",
    )
