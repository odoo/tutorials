from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag to be applied to a property"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _name_uniq = models.Constraint(
        "UNIQUE(name)",
        "A property tag with this name already exists!",
    )
