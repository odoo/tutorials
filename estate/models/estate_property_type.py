from odoo import fields, models


class Type(models.Model):
    _name = "estate.property.type"
    _description = "Type of property of Estate"

    name = fields.Char(required=True)

    _uniq_name = models.Constraint(
        "unique(name)",
        "A Type name should be unique.",
    )
