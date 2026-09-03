from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "The property tag name must be unique.",
    )
