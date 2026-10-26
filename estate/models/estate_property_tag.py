from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "The name of a tag should be unique.",
    )
