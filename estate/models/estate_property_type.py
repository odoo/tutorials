from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property types"

    name = fields.Char("Type", required=True)

    _uniq_name = models.Constraint(
        "UNIQUE(name)",
        "This name is already taken",
    )
