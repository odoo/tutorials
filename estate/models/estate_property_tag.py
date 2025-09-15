from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tag"
    _order = "name"

    _check_tag_name = models.Constraint(
        "UNIQUE(name)",
        "The property tag name must be unique.",
    )

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")
