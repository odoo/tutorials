from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char('Name', required=True)

    _name_must_be_unique = models.Constraint(
        "UNIQUE(name)",
        "Tag name must be unique",
    )
