from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    _sql_name_unique = models.Constraint(
        "UNIQUE(name)",
        "Property tag already exists.",
    )