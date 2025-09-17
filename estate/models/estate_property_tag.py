from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer("Color Index")

    _sql_constraints = [
        (
            "name_uniq",
            "unique(name)",
            "A tag with the same name exists.",
        )
    ]
