from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Tag Description"

    name = fields.Char(required=True)

    _name_unique = models.Constraint(
        "UNIQUE(name)",
        "The name must be unique.",
    )
