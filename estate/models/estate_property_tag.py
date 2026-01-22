from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char("Name", required=True)

    _unique_name = models.Constraint(
        "UNIQUE (name)",
        "A property tag name must be unique",
    )
