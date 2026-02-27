from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"
    color = fields.Integer("Color")
    name = fields.Char(required=True)

    _check_name_unique = models.Constraint(
        "UNIQUE(name)",
        "The property tag name must be unique.",
    )
