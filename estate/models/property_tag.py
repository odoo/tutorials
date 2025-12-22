from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char("Tag Name", required=True)
    color = fields.Integer("Color")

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "The property tag name must be unique"
    )
