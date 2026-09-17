from odoo import fields, models


class Type(models.Model):
    _name = "estate.property.tag"
    _description = "Tag of property of Estate"

    name = fields.Char(required=True)

    _uniq_name = models.Constraint(
        "unique(name)",
        "A tag name should be unique.",
    )
