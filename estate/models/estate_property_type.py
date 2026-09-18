from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)

    _unique_constraints = models.Constraint(
        definition='UNIQUE(name)',
        message='The property type name must be unique',
    )
