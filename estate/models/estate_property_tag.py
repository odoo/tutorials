from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag representing an attribute's presence in a property"
    _order = "name"

    active = fields.Boolean(default=True)
    color = fields.Integer(string="Color")
    name = fields.Char(required=True)

    _name_uniq = models.Constraint(
        "unique (name)",
        "Each tag name must be unique.",
    )
