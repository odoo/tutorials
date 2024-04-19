from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate property tag"
    _order = "name"
    _sql_constraints = [
        (
            "unique_property_tag",
            "UNIQUE(name)",
            "The property tag must be unique",
        )
    ]

    name = fields.Char("Name", required=True)
    color = fields.Integer()
