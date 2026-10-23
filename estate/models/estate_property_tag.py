from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tags"

    name = fields.Char("Name", required=True)

    _uniq_name = models.Constraint(
        "UNIQUE(name)",
        "This name is already taken",
    )
