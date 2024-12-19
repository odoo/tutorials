from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"
    _sql_constraints = [
        (
            "name",
            "unique(name)",
            "The property tag must be unique.",
        )
    ]

    name = fields.Char(required=True)
    color = fields.Integer()
