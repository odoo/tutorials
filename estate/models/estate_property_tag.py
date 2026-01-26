from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag to be applied to a property"

    name = fields.Char(required=True)

    _name_uniq = models.Constraint(
        "UNIQUE(name)",
        "A property tag with this name already exists!",
    )
