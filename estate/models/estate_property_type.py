from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "property types"

    name = fields.Char(required=True)

    _unique_name = models.Constraint(
        'unique(name)',
        'A property type must have a unique name.',
    )
