from odoo import models, fields


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(string="Name", required=True)
    _name_uniq = models.Constraint(
        "UNIQUE (name)",
        "The name of the tag must be unique!",
    )
