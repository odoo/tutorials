from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char('Property Types', required=True)

    _name_must_be_unique = models.Constraint(
        "UNIQUE(name)",
        "Property type name must be unique",
    )
