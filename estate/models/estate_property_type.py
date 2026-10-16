from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(required=True)

    _type_name_uniq = models.Constraint(
        'unique (name)',
        'The type name must be unique.',
    )
