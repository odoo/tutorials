from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "property.tag"
    _description = "Property Tags"
    _order = "name"

    _sql_constraints = [
        (
            "property_tag_name_unique",
            "UNIQUE(name)",
            "The property tag name must be unique.",
        )
    ]

    name = fields.Char("Name")
    color = fields.Integer("Color", default=0)
