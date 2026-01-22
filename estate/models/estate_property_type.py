from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(required=True)

    _unique_type_name = models.Constraint(
        'UNIQUE(name)',
        'The property type name must be unique.',
    )
