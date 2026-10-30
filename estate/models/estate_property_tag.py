from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char('Name', required=True)
    color = fields.Integer()

    _name_must_be_unique = models.Constraint(
        "UNIQUE(name)",
        "Tag name must be unique",
    )
