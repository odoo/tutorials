from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name asc"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer()

    _name_uniq = models.Constraint(
        "UNIQUE (name)",
        "The name of the tag must be unique!",
    )
