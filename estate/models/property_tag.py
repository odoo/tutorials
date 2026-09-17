from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate property tags"

    name = fields.Char(required=True)

    _name_uniq = models.Constraint(
        "unique(name)",
        "A tag with the same name already exists",
    )
